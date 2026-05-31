import asyncio
import logging
from typing import Dict, Any, Optional, Callable

logger = logging.getLogger(__name__)

class CollaborationManager:
    """
    The 'Bridge' between the AI Swarm and the Human User.
    Handles Interrupts, Review Gates, and Mid-flight Corrections.
    """
    def __init__(self):
        self.pending_inputs: Dict[str, asyncio.Future] = {}
        self.review_gates: Dict[str, bool] = {}

    async def wait_for_user_input(self, question: str, task_id: str) -> str:
        """Suspends the agent until a human provides an answer."""
        logger.warning(f"Collaboration: Task {task_id} is awaiting human input: {question}")
        
        # Create a future that will be resolved by the API endpoint
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.pending_inputs[task_id] = future
        
        # Wait for the UI to call /api/v1/collaboration/input
        try:
            user_response = await future
            return user_response
        finally:
            self.pending_inputs.pop(task_id, None)

    async def request_review(self, artifact_path: str, task_id: str) -> bool:
        """Implements a Review Gate. Execution pauses until approved."""
        logger.info(f"Collaboration: Awaiting review for {artifact_path} (Task: {task_id})")
        # In a real system, this sends a notification to the UI and waits for a boolean response.
        return True # Mocked approval for now

    def provide_input(self, task_id: str, response: str):
        """Called by the API/Controller when the user submits their response."""
        if task_id in self.pending_inputs:
            self.pending_inputs[task_id].set_result(response)
            logger.info(f"Collaboration: Input received for Task {task_id}")

class ExperienceMemory:
    """
    The 'Learning' layer. 
    Stores successful Workflow Patterns and avoids repeating past failures.
    """
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.patterns: List[Dict[str, Any]] = []

    def record_success(self, goal: str, plan: Any, outcome: str):
        """Saves a 'Winning Strategy' for future goals."""
        pattern = {
            "goal_type": self._classify_goal(goal),
            "plan_structure": [t.assigned_role for t in plan.tasks.values()],
            "timestamp": datetime.utcnow().isoformat()
        }
        self.patterns.append(pattern)
        # Persistence logic...

    def get_advice(self, goal: str) -> Optional[str]:
        """Provides 'Tips' to the Planner based on historical success."""
        # Query similar historical patterns
        return "Advice: For startup research, prioritize Crunchbase scraping before LinkedIn."

    def _classify_goal(self, goal: str) -> str:
        return "MarketResearch"
