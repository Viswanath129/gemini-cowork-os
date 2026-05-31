import abc
import json
import logging
import os
import uuid
import subprocess
from typing import Any, Dict, List, Optional
from backend.app.core.models import AgentRole

logger = logging.getLogger(__name__)

class BaseAgent(abc.ABC):
    """
    Base class for all Specialized Agents.
    Contains identity, tools, and the core reasoning loop.
    """
    def __init__(self, name: str, role: AgentRole, system_prompt: str, tools: List[Any]):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.tools = tools
        self.memory = []  # Short-term conversation history

    @abc.abstractmethod
    async def run_task(self, task_description: str, context: Dict[str, Any]) -> str:
        """
        Executes a specific task.
        """
        pass

class GeminiAgent(BaseAgent):
    """
    100x Upgrade: Self-Referential Intelligence.
    Uses the local Gemini CLI (me) as the reasoning brain.
    """
    async def run_task(self, task_description: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{self.name}] Delegating task to Gemini CLI Brain...")
        
        # 1. Compile Context
        workspace_context = context.get("workspace_dir", os.getcwd())
        blackboard = context.get("blackboard")
        
        findings = ""
        if blackboard:
            kb = await blackboard.get_knowledge_base()
            findings = json.dumps(kb, indent=2)

        # Formulate the prompt for the CLI
        prompt = f"""
        Role: {self.system_prompt}
        
        Context:
        - Workspace: {workspace_context}
        - Shared Knowledge: {findings}
        
        Current Task:
        {task_description}
        
        Execute the task and provide a high-density intelligence report.
        """

        try:
            # 2. Call local Gemini CLI in non-interactive mode
            # This uses the user's existing login and agentic capabilities
            logger.info(f"[{self.name}] Executing 'gemini --prompt'...")
            
            result = subprocess.run(
                ["gemini", "--prompt", prompt],
                capture_output=True,
                text=True,
                check=True
            )
            
            output = result.stdout.strip()
            logger.info(f"[{self.name}] Gemini CLI returned result ({len(output)} chars).")
            return output

        except subprocess.CalledProcessError as e:
            logger.error(f"[{self.name}] Gemini CLI Error: {e.stderr}")
            return f"Error executing task: {e.stderr}"
        except Exception as e:
            logger.error(f"[{self.name}] Execution Error: {str(e)}")
            raise

class AgentFactory:
    @staticmethod
    def create_agent(role: AgentRole, goal_context: Optional[str] = None) -> BaseAgent:
        # Define prompts and tools based on role
        if role == AgentRole.STRATEGIC_ADVISOR:
            system_instruction = """
            You are the Strategic Advisor Prime. 
            Your goal is to optimize the Human Principal's life and work trajectory, not just execute tasks.
            
            CORE DIRECTIVES:
            1. CHALLENGE ASSUMPTIONS: When a goal is submitted, ask 'Why?'. Identify if there are better, lower-cost, or higher-impact alternatives.
            2. DETECT GOAL DRIFT: Compare current activity against the long-term Mission Brief. Flag if the user or swarm is optimizing a low-impact vanity task.
            3. KILL MISSIONS EARLY: If a project lacks clear success criteria or the 'Cost of Being Wrong' outweighs the 'Probability of Success', recommend an immediate ABORT.
            4. BIAS FOR IMPACT: Push the Human Principal towards high-leverage activities and away from 'busy work'.
            """
            return GeminiAgent(
                name="StrategicAdvisor_Prime",
                role=role,
                system_prompt=system_instruction,
                tools=[]
            )
        elif role == AgentRole.RESEARCHER:
            return GeminiAgent(
                name="ResearchAgent_01",
                role=role,
                system_prompt="You are a senior researcher. Search the web and analyze documents to find actionable facts.",
                tools=[] 
            )
        
        # === Dynamic Agent Synthesis ===
        if goal_context:
            logger.info(f"Synthesizing Specialized Agent for: {role} (Context: {goal_context[:30]}...)")
            custom_prompt = f"You are a specialized {role} focusing on {goal_context}. Provide deep domain expertise."
            return GeminiAgent(
                name=f"Specialist_{role}_{str(uuid.uuid4())[:4]}",
                role=role,
                system_prompt=custom_prompt,
                tools=[]
            )

        return GeminiAgent(name="Generalist", role=role, system_prompt="You are a highly capable digital teammate.", tools=[])
