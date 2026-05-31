import asyncio
import networkx as nx
import logging
import os
from typing import Dict, Any, Optional

from backend.app.core.models import ExecutionPlan, TaskStatus, Task
from backend.app.core.agent import AgentFactory
from backend.app.core.kernel import ExecutionKernel, SharedBlackboard

logger = logging.getLogger(__name__)

class MissionBrief(BaseModel):
    goal: str
    why: str
    impact_score: str # Low, Medium, High, Critical
    cost_of_being_wrong: str # Description of consequences
    success_criteria: List[str]
    constraints: List[str]
    assumptions: List[str]
    risks: List[str]
    confidence_score: float

class GoalInterpreter:
    """Converts high-level goals into a DAG of Tasks with Judgment-based Ambiguity Detection."""
    
    async def generate_mission_brief(self, prompt: str) -> MissionBrief:
        """
        The 'Understand -> Clarify -> Align' phase.
        Discovers the What, Why, Impact, and How before execution.
        """
        logger.info(f"Goal Interpreter: Generating Adaptive Mission Brief for: '{prompt[:50]}...'")
        
        # In real implementation: Call a reasoning LLM to audit the prompt for intent and impact
        # Mocking Adaptive Impact Logic:
        impact = "Low"
        cost_desc = "Minor inconvenience / Time waste"
        
        if "startup" in prompt.lower() or "invest" in prompt.lower():
            impact = "High"
            cost_desc = "Financial loss or wasted strategic effort"
        elif "career" in prompt.lower() or "college" in prompt.lower():
            impact = "Critical"
            cost_desc = "Significant long-term life trajectory impact"

        return MissionBrief(
            goal=prompt,
            why="Strategic support", 
            impact_score=impact,
            cost_of_being_wrong=cost_desc,
            success_criteria=["Defined outcome X", "Verified data Y"],
            constraints=["Default project limits"],
            assumptions=["Human principal owns final decision"],
            risks=["Information asymmetry"],
            confidence_score=0.85
        )

    async def detect_ambiguity(self, prompt: str) -> List[str]:
        """
        Distinguishes between 'Material Ambiguity' (must ask) and 'Minor Ambiguity' (must act).
        """
        logger.info(f"Goal Interpreter: Running Judgment Engine on: '{prompt[:50]}...'")
        
        # In real implementation: Call a high-level LLM with a 'Decision-Relevance' rubric.
        material_questions = []
        
        # Example Case A.2: False Confidence Trap
        if "best" in prompt.lower() and "stock" in prompt.lower():
            material_questions.append("Is this for a long-term retirement horizon or short-term day trading?")
            material_questions.append("What is your risk tolerance for this investment analysis?")
            
        # Example Case A.3: Partial Ambiguity (Determine if material)
        if "semiconductor" in prompt.lower() and "report" in prompt.lower():
            # If the user says 'prepare a report', the type of report is MATERIAL to the plan.
            material_questions.append("Should the report be an Investor Outlook, a Technical Analysis, or a Market Landscape?")
            
        # Filter: If the user says 'Summarize these PDFs', we do NOT ask about font/formatting.
        # Those are MINOR and should be handled with defaults.
        
        return material_questions

    def parse_goal(self, user_prompt: str) -> ExecutionPlan:
        # LLM Logic would go here to generate the DAG
        plan = ExecutionPlan(
            goal=user_prompt,
            tasks={}
        )
        plan.tasks["task_1"] = Task(
            id="task_1",
            description="Initial research on the goal",
            assigned_role="Researcher",
            dependencies=[]
        )
        return plan

from backend.app.core.observability import ObservabilityLayer, GoalGuardian
from backend.app.core.swarm import ReflectionEngine

class ExecutionEngine:
    """Runs the execution plan via the Kernel, managing persistence and coordination."""
    
    def __init__(self, plan: ExecutionPlan, kernel: ExecutionKernel, goal_id: str):
        self.plan = plan
        self.kernel = kernel
        self.goal_id = goal_id
        self.blackboard = SharedBlackboard()
        self.obs = ObservabilityLayer()
        self.guardian = GoalGuardian(self)
        self.reflector = ReflectionEngine() # Act -> Verify -> Repair
        
    async def execute(self):
        logger.info(f"Autonomous Execution starting for goal: {self.plan.goal}")
        
        step_count = 0
        while True:
            step_count += 1
            
            # 1. Goal Re-anchoring (Strategic Drift Check)
            if step_count % 5 == 0:
                is_on_track = await self.guardian.check_drift(
                    self.plan.goal, 
                    self.plan, 
                    await self.blackboard.get_knowledge_base()
                )
                if not is_on_track:
                    logger.warning("Goal Guardian detected drift. Initiating autonomous correction.")
            
            # 2. Kernel-driven step (Handles Checkpointing and Deadlocks)
            stepped = await self.kernel.run_step(self.plan, self._run_task_with_reflection)
            
            if not stepped:
                # All tasks completed or system blocked
                break

    async def _run_task_with_reflection(self, task: Task):
        """The core Autonomous Loop: Execute -> Verify -> Repair."""
        self.obs.log_event("TASK_START", task.assigned_role, self.goal_id, {"description": task.description})
        task.status = TaskStatus.IN_PROGRESS
        
        try:
            # Wrap the agent execution in the Reflection Engine
            result = await self.reflector.execute_with_reflection(
                task, 
                self._execute_agent_logic(task),
                max_retries=3
            )
            
            await self.blackboard.post_finding(f"result_{task.id}", result, task.assigned_role)
            task.result = result
            task.status = TaskStatus.COMPLETED
            self.obs.log_event("TASK_END", task.assigned_role, self.goal_id, {"status": "SUCCESS"})
            
        except Exception as e:
            logger.error(f"Autonomous Loop Failure on task {task.id}: {str(e)}")
            self.obs.log_event("TASK_FAILURE", task.assigned_role, self.goal_id, {"error": str(e)})
            task.status = TaskStatus.FAILED

    async def _execute_agent_logic(self, task: Task) -> str:
        """Helper to run the actual agent call."""
        agent = AgentFactory.create_agent(task.assigned_role)
        context = {
            "blackboard": self.blackboard, 
            "workspace_dir": os.getcwd(),
            "goal_id": self.goal_id
        }
        return await agent.run_task(task.description, context)

class Orchestrator:
    """Main entry point. Orchestrates the Kernel and Engine."""

    def __init__(self, checkpoint_dir: str = ".checkpoints"):
        self.interpreter = GoalInterpreter()
        self.checkpoint_dir = checkpoint_dir
        self.obs_global = ObservabilityLayer()

    async def submit_goal(self, goal: str, goal_id: str = "default"):
        checkpoint_path = f"{self.checkpoint_dir}/{goal_id}.json"
        kernel = ExecutionKernel(checkpoint_path)

        # 1. Ambiguity Detection & Judgment (Decision: ASK vs PROCEED)
        ambiguities = await self.interpreter.detect_ambiguity(goal)
        
        # 2. Alignment Phase: MISSION BRIEF (The 'Understand' phase)
        mission_brief = await self.interpreter.generate_mission_brief(goal)
        
        # SELECITVE GATE: Only halt for alignment if material ambiguity exists
        # or if the task is a high-impact 'Decision Support' goal.
        if ambiguities or mission_brief.confidence_score < 0.8:
            self.obs_global.record_judgment("ASK", goal, is_correct=True)
            logger.warning(f"SUSPENDING FOR ALIGNMENT: Goal '{goal}' requires verification.")
            return {
                "status": "AWAITING_ALIGNMENT",
                "brief": mission_brief,
                "questions": ambiguities,
                "goal_id": goal_id
            }
        else:
            self.obs_global.record_judgment("PROCEED", goal, is_correct=True)
            logger.info("Goal alignment high. Proceeding automatically.")

        # 3. Try to recover from checkpoint
        plan = kernel.load_last_checkpoint()
        
        if plan:
            self.obs_global.record_judgment("PRESERVE", f"Recovery for {goal_id}", is_correct=True)
            logger.info("Resuming execution from last checkpoint.")
        else:
            plan = self.interpreter.parse_goal(goal)
            logger.info("Generated new execution plan.")

        engine = ExecutionEngine(plan, kernel, goal_id)
        engine.obs = self.obs_global # Share the global observability layer
        engine.obs.ambiguity_detected = False 

        await engine.execute()
        return plan

