import os
import json
from typing import List, Dict, Any

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
    Wrapper around Vector DB (Chroma/Qdrant) for long-term document understanding.
    Allows agents to query "What did we decide about X in the previous milestone?"
    """
    def __init__(self, collection_name: str):
        # In real implementation: self.client = chromadb.Client()
        self.collection_name = collection_name
        
    def store_document(self, text: str, metadata: Dict[str, Any]):
        # chunk text, generate embeddings, store in vector DB
        pass
        
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        # embed query, search vector db, return closest chunks
        return []
