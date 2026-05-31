import os
import json
import logging
import chromadb
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ProjectMemory:
    """
    Handles local file-system/SQLite memory storage for a specific project.
    """
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.memory_dir = os.path.join(project_path, ".memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        
    def save_fact(self, key: str, value: Any):
        path = os.path.join(self.memory_dir, f"{key}.json")
        with open(path, 'w') as f:
            json.dump({"fact": value}, f)
            
    def load_fact(self, key: str) -> Any:
        path = os.path.join(self.memory_dir, f"{key}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f).get("fact")
        return None

class SemanticMemory:
    """
    100x Upgrade: Real Vector Database integration using ChromaDB.
    Allows agents to query historical decisions and deep document archives.
    """
    def __init__(self, collection_name: str, db_path: str = "./.chromadb"):
        logger.info(f"Initializing ChromaDB Vector Store at {db_path}...")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        
    def store_document(self, text: str, metadata: Dict[str, Any], doc_id: str):
        """Embeds and stores document chunks in the vector DB."""
        logger.info(f"Storing vector chunk: {doc_id}")
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Queries the vector DB for semantically relevant chunks."""
        logger.info(f"Performing semantic search: '{query}'")
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format results for the Agent
        formatted_results = []
        if results and "documents" in results and results["documents"]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i]
                })
        return formatted_results
