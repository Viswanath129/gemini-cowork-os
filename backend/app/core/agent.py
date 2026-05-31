import abc
import json
import logging
import os
import uuid
import google.generativeai as genai
from typing import Any, Dict, List, Optional
from backend.app.core.models import AgentRole

logger = logging.getLogger(__name__)

# Configure Real Gemini API (Requires GEMINI_API_KEY environment variable)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "mock_key"))

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
        Executes a specific task. Uses LLM to decide which tools to call.
        """
        pass

class GeminiAgent(BaseAgent):
    """
    Concrete implementation of an Agent powered by actual Google Gemini API.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize the actual Gemini 1.5 Pro model for massive context and complex reasoning
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            system_instruction=self.system_prompt
        )

    async def run_task(self, task_description: str, context: Dict[str, Any]) -> str:
        logger.info(f"[{self.name}] Starting task via Gemini API: {task_description[:50]}...")
        
        # 1. Compile Context (Workspace, Blackboard)
        workspace_context = context.get("workspace_dir", "Unknown workspace")
        blackboard = context.get("blackboard")
        
        findings = ""
        if blackboard:
            kb = await blackboard.get_knowledge_base()
            findings = json.dumps(kb, indent=2)

        prompt = f"""
        TASK TO EXECUTE:
        {task_description}

        WORKSPACE CONTEXT: {workspace_context}
        
        EXISTING KNOWLEDGE (Blackboard):
        {findings}
        
        Execute the task and return the final detailed result.
        """

        try:
            # 2. Actual API Call to Gemini
            if os.environ.get("GEMINI_API_KEY"):
                response = self.model.generate_content(prompt)
                result = response.text
                logger.info(f"[{self.name}] Task completed successfully via Gemini.")
                return result
            else:
                # Safe fallback if no key is set so the local repo doesn't crash instantly
                logger.warning(f"[{self.name}] GEMINI_API_KEY not found. Simulating response.")
                return f"[{self.name}] Simulated execution for: {task_description}"

        except Exception as e:
            logger.error(f"[{self.name}] Gemini API Error: {str(e)}")
            raise

class AgentFactory:
    @staticmethod
    def create_agent(role: AgentRole, goal_context: Optional[str] = None) -> BaseAgent:
        if role == AgentRole.RESEARCHER:
            return GeminiAgent(
                name="ResearchAgent_01",
                role=role,
                system_prompt="You are a senior researcher. Synthesize complex data into high-density actionable intelligence.",
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

        return GeminiAgent(name="Generalist", role=role, system_prompt="You are a highly capable generalist AI coworker.", tools=[])