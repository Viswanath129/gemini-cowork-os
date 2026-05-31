from typing import Any, Callable, Dict, Type
from pydantic import BaseModel
import inspect

class Tool(BaseModel):
    name: str
    description: str
    requires_approval: bool = False
    func: Callable
    schema: Type[BaseModel]

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        return self._tools.get(name)

    def execute_tool(self, name: str, kwargs: Dict[str, Any]) -> Any:
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool {name} not found.")
        
        if tool.requires_approval:
            # In a real system, this raises an exception caught by the orchestrator 
            # to suspend the DAG and alert the UI.
            raise InterruptedError(f"Tool {name} requires human approval.")
        
        return tool.func(**kwargs)

# === Example Built-in Tools ===

class WriteFileSchema(BaseModel):
    filepath: str
    content: str

def write_file_impl(filepath: str, content: str) -> str:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"Successfully wrote to {filepath}"

write_file_tool = Tool(
    name="write_file",
    description="Writes text content to a specific file on the disk.",
    requires_approval=False, # Safe in sandbox
    func=write_file_impl,
    schema=WriteFileSchema
)

class DeleteFileSchema(BaseModel):
    filepath: str

def delete_file_impl(filepath: str) -> str:
    import os
    os.remove(filepath)
    return f"Deleted {filepath}"

delete_file_tool = Tool(
    name="delete_file",
    description="Deletes a file permanently. MUST ASK USER FIRST.",
    requires_approval=True, # STRICT SECURITY LAYER
    func=delete_file_impl,
    schema=DeleteFileSchema
)
