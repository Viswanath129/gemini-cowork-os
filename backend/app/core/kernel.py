import json
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from backend.app.core.models import ExecutionPlan, TaskStatus, Task

logger = logging.getLogger(__name__)

class ExecutionKernel:
    """
    The 'OS Kernel' for Cowork. 
    Handles:
    - Task Scheduling
    - State Checkpointing (Persistence)
    - Recovery (Resuming from failure/restart)
    - Deadlock Detection
    """
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        import os
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def save_checkpoint(self, plan: ExecutionPlan):
        """Snapshots the entire DAG state to persistent storage."""
        data = plan.model_dump()
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Checkpoint saved: {len(plan.tasks)} tasks synchronized.")

    def load_last_checkpoint(self) -> Optional[ExecutionPlan]:
        """Recovers the last known state of the Execution DAG."""
        import os
        if not os.path.exists(self.storage_path):
            return None
        
        with open(self.storage_path, 'r') as f:
            data = json.load(f)
            logger.info("Recovering Execution Plan from checkpoint...")
            return ExecutionPlan(**data)

    def detect_deadlock(self, plan: ExecutionPlan) -> bool:
        """
        Scans the DAG for circular dependencies or starvation.
        """
        # 1. Check for 'IN_PROGRESS' tasks that haven't updated in X minutes (Starvation)
        # 2. Check for circular dependencies in 'PENDING' tasks
        # (Simplified implementation for scaffold)
        return False 

    async def run_step(self, plan: ExecutionPlan, execute_task_fn):
        if self.detect_deadlock(plan):
            logger.error("Deadlock detected in Execution DAG! Initiating recovery...")
            return False

        runnable = plan.get_runnable_tasks()
        if not runnable:
            return False

        self.save_checkpoint(plan)
        import asyncio
        await asyncio.gather(*[execute_task_fn(task) for task in runnable])
        self.save_checkpoint(plan)
        return True

class SharedBlackboard:
    """
    Coordination Layer for Agent Swarms.
    Includes Promotion logic to separate 'Working Memory' from 'Canonical Knowledge'.
    """
    def __init__(self):
        self._findings: Dict[str, Any] = {} # Working Memory
        self._canonical: Dict[str, Any] = {} # Validated Findings
        self._lock = asyncio.Lock()

    async def post_finding(self, key: str, value: Any, agent_id: str):
        async with self._lock:
            self._findings[key] = {
                "content": value,
                "agent": agent_id,
                "timestamp": datetime.utcnow().isoformat(),
                "validated": False
            }
            logger.info(f"Blackboard Update: {agent_id} posted working finding '{key}'")

    async def promote_to_canonical(self, key: str, validator_agent_id: str):
        """Promotes a finding to Canonical Knowledge after validation."""
        async with self._lock:
            if key in self._findings:
                finding = self._findings.pop(key)
                finding["validated"] = True
                finding["validator"] = validator_agent_id
                self._canonical[key] = finding
                logger.info(f"Knowledge Promotion: '{key}' is now Canonical.")

    async def get_knowledge_base(self) -> Dict[str, Any]:
        """Returns only validated knowledge."""
        return self._canonical
