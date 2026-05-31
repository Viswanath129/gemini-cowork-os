import asyncio
import logging
from typing import List, Dict, Any, Callable, Coroutine
from backend.app.core.models import Task, TaskStatus
from backend.app.core.agent import AgentFactory

logger = logging.getLogger(__name__)

class AgentSwarm:
    """
    Manages a pool of parallel worker agents to handle high-volume tasks.
    Example: Processing 1000 PDFs by splitting them into batches for N parallel agents.
    """
    def __init__(self, role: str, max_parallel: int = 5):
        self.role = role
        self.max_parallel = max_parallel
        self.semaphore = asyncio.Semaphore(max_parallel)

    async def map_reduce(self, items: List[Any], task_description: str, context: Dict[str, Any]) -> List[str]:
        """
        Executes a task description across a list of items in parallel.
        """
        logger.info(f"Swarm [{self.role}] starting parallel processing of {len(items)} items.")
        
        async def _worker(item: Any):
            async with self.semaphore:
                agent = AgentFactory.create_agent(self.role)
                # Specialized sub-task for this specific item
                specific_task = f"{task_description} | Target Item: {str(item)}"
                result = await agent.run_task(specific_task, context)
                return result

        # Launch all workers in parallel
        results = await asyncio.gather(*[_worker(item) for item in items])
        return results

from backend.app.core.models import Task, TaskStatus, AgentRole

class ReflectionEngine:
    """
    Implements the Plan -> Execute -> Critique -> Repair loop.
    Ensures agents don't just 'finish', but 'succeed'.
    """
    def __init__(self, obs=None, critique_agent_role: AgentRole = AgentRole.COORDINATOR):
        self.critique_agent = AgentFactory.create_agent(critique_agent_role)
        self.obs = obs

    async def execute_with_reflection(self, task: Task, execution_factory: Callable[[], Coroutine], max_retries: int = 3) -> str:
        attempt = 0
        current_result = ""
        initial_failed = False
        
        while attempt < max_retries:
            attempt += 1
            logger.info(f"Reflection Loop: Attempt {attempt} for task {task.id}")
            
            # 1. Execute via factory to get fresh coroutine
            current_result = await execution_factory()
            
            # 2. Critique
            critique_prompt = f"""
            Task Goal: {task.description}
            Produced Output: {current_result}
            
            Evaluate the output against the goal. 
            Identify missing information, errors, or formatting issues.
            Return 'PASSED' if perfect, otherwise provide detailed 'REPAIR_INSTRUCTIONS'.
            """
            critique = await self.critique_agent.run_task(critique_prompt, {})
            logger.info(f"Critique Output: '{critique}'")
            
            if "PASSED" in critique.upper():
                logger.info(f"Task {task.id} passed reflection.")
                if initial_failed and self.obs:
                    # Successfully repaired!
                    self.obs.record_repair(improved=True)
                elif self.obs:
                    self.obs.first_attempt_passes += 1
                return current_result
            
            initial_failed = True
            logger.warning(f"Task {task.id} failed critique. Repairing based on: {critique[:100]}...")
            
            # Scenario Check for Degradation (Simulation)
            if "Error" in current_result and "Error" in critique:
                 if self.obs: self.obs.record_repair(improved=False, worsened=True)
            
            # 3. Repair - modify the next execution attempt with the critique
            task.description = f"{task.description}\n\nPREVIOUS_CRITIQUE: {critique}"
            
        return current_result
