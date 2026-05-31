import logging
from typing import List, Dict, Any
from backend.app.core.agent import AgentFactory

logger = logging.getLogger(__name__)

class ContextCompressor:
    """
    Prevents Context Window Explosion.
    Implements Hierarchical Summarization: Raw Docs -> Chunks -> Summaries -> Knowledge Graph.
    """
    def __init__(self):
        self.summarizer = AgentFactory.create_agent("Researcher")

    async def compress_documents(self, raw_contents: List[str]) -> str:
        """
        Takes thousands of pages and compresses them into a high-density executive summary.
        """
        # Phase 1: Chunk-level summarization
        logger.info(f"Compressing {len(raw_contents)} document streams...")
        chunk_summaries = []
        for content in raw_contents:
            summary = await self.summarizer.run_task(
                f"Extract only critical facts, data points, and decisions from this text: {content[:5000]}", 
                {}
            )
            chunk_summaries.append(summary)
            
        # Phase 2: Recursive Merging
        final_context = await self.summarizer.run_task(
            f"Synthesize these partial summaries into a single hierarchical knowledge structure:\n\n" + 
            "\n---\n".join(chunk_summaries),
            {}
        )
        
        return final_context

class WorkspaceManager:
    """
    Manages the 'Operating System' state above individual projects.
    Handles shared memory, team context, and cross-project deliverables.
    """
    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.workspaces_path = f"{root_dir}/workspaces"
        
    def get_workspace_context(self, workspace_id: str) -> Dict[str, Any]:
        """Loads shared team rules, global agent history, and cross-project patterns."""
        return {
            "shared_knowledge": f"{self.workspaces_path}/{workspace_id}/shared_memory.db",
            "global_preferences": ["Use Metric system", "Tone: Professional", "Format: Markdown First"]
        }
