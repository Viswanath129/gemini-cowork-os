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
        
        # Judgment & Behavioral Metrics
        self.judgment_decisions: List[Dict[str, Any]] = [] # Records: {type: 'ASK|PROCEED|REPLAN', is_correct: bool}
        self.ambiguity_detected = False
        self.clarification_questions: List[str] = []
        self.useful_questions_count = 0
        self.premature_work_seconds = 0.0
        self.preserved_findings_count = 0
        self.discarded_useful_findings_count = 0
        self.total_findings_pre_pivot = 0

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
