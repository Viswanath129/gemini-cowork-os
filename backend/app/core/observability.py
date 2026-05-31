import time
import logging
from typing import Dict, Any, List
from pydantic import BaseModel
from datetime import datetime

logger = logging.getLogger(__name__)

class TelemetryEvent(BaseModel):
    timestamp: datetime = datetime.utcnow()
    event_type: str # TASK_START, TASK_END, TOOL_CALL, TOKEN_USAGE, COST
    agent_id: str
    goal_id: str
    metadata: Dict[str, Any]

class ObservabilityLayer:
    """
    The 'Black Box Recorder' and Monitor for Cowork OS.
    Tracks performance, costs, and execution traces.
    """
    def __init__(self):
        self.events: List[TelemetryEvent] = []
        self.total_tokens = 0
        self.total_cost = 0.0
        self.useful_work_seconds = 0.0
        self.total_work_seconds = 0.0
        self.user_satisfaction_score: Optional[float] = None
        
        # Empirical Validation Metrics
        self.total_tasks = 0
        self.verified_tasks_completed = 0 # ACS Numerator
        self.human_touch_count = 0 # HTC
        self.repair_attempts = 0
        self.repair_successes = 0 # Moved from fail to pass
        self.repair_degradations = 0 # Made output worse
        self.first_attempt_passes = 0
        
        # Judgment & Behavioral Metrics
        self.judgment_decisions: List[Dict[str, Any]] = [] 
        self.ambiguity_detected = False
        self.clarification_questions: List[str] = []

    def record_repair(self, improved: bool, worsened: bool = False):
        self.repair_attempts += 1
        if improved:
            self.repair_successes += 1
        if worsened:
            self.repair_degradations += 1

    def get_repair_efficacy(self) -> Dict[str, Any]:
        """Detailed metrics on whether autonomous repairs are working."""
        total = self.repair_attempts
        if total == 0:
            return {"status": "NO_REPAIRS"}
        return {
            "total_attempts": total,
            "success_rate": self.repair_successes / total,
            "degradation_rate": self.repair_degradations / total
        }

    def get_autonomous_completion_score(self) -> float:
        """ACS = Verified Tasks Completed / Total Tasks"""
        if self.total_tasks == 0:
            return 1.0
        return self.verified_tasks_completed / self.total_tasks

    def record_judgment(self, decision_type: str, context: str, is_correct: bool):
        """Logs a judgment call (ASK, PROCEED, REPLAN, PRESERVE, REFUSE, DEFER)."""
        self.judgment_decisions.append({
            "type": decision_type,
            "context": context,
            "is_correct": is_correct,
            "timestamp": datetime.utcnow().isoformat()
        })

    def get_refusal_quality_score(self) -> float:
        """Formula: Correct Refuse/Defer decisions / Total Refuse/Defer decisions"""
        refusal_types = ["REFUSE", "DEFER", "ABORT"]
        refusals = [d for d in self.judgment_decisions if d["type"] in refusal_types]
        if not refusals:
            return 1.0
        correct_refusals = sum(1 for d in refusals if d["is_correct"])
        return correct_refusals / len(refusals)

    def get_judgment_accuracy_score(self) -> float:
        """Formula: Correct Decisions / Total Judgment Decisions"""
        total = len(self.judgment_decisions)
        if total == 0:
            return 1.0
        correct = sum(1 for d in self.judgment_decisions if d["is_correct"])
        return correct / total

    def log_event(self, event_type: str, agent_id: str, goal_id: str, metadata: Dict[str, Any]):
        event = TelemetryEvent(
            event_type=event_type,
            agent_id=agent_id,
            goal_id=goal_id,
            metadata=metadata
        )
        self.events.append(event)
        
        # Track usage
        if "tokens" in metadata:
            self.total_tokens += metadata["tokens"]
        if "cost" in metadata:
            self.total_cost += metadata["cost"]
            
        # Track Premature Execution
        if event_type == "TASK_START" and self.ambiguity_detected:
            # If a task starts while ambiguity is still flagged, it's premature.
            logger.warning(f"PREMATURE EXECUTION: Agent {agent_id} started despite ambiguity.")

        # Track Work Ratios
        if event_type == "TASK_END":
            latency = metadata.get("latency", 0.0)
            self.total_work_seconds += latency
            if not metadata.get("is_wasted", False):
                self.useful_work_seconds += latency
            
        logger.info(f"Observability: [{event_type}] {agent_id} | Cost: ${self.total_cost:.4f}")

class GoalGuardian:
    """
    The 'Anchor' Agent.
    Periodically checks if the swarm is drifting from the original objective.
    """
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    async def check_drift(self, goal: str, current_plan: Any, blackboard_findings: Dict[str, Any]) -> bool:
        """
        Runs a re-alignment check. 
        Returns True if on track, False if significant drift detected.
        """
        logger.info("Goal Guardian: Running re-alignment check...")
        
        # In real implementation: Call a high-level LLM (e.g. Gemini Ultra)
        # to compare Goal vs. Completed Tasks vs. Current Plan.
        
        # If drift detected: 
        # self.orchestrator.replan(goal, reason="Detected drift in research scope.")
        return True
