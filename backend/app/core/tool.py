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

class PythonExecutorSchema(BaseModel):
    code: str

def python_executor_impl(code: str) -> str:
    """Executes arbitrary python code in a separate process."""
    import subprocess
    import sys
    try:
        # Save to temp file and run
        with open("mission_temp_script.py", "w") as f:
            f.write(code)
        result = subprocess.run([sys.executable, "mission_temp_script.py"], capture_output=True, text=True, timeout=30)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Python Execution Failed: {str(e)}"
    finally:
        if os.path.exists("mission_temp_script.py"): os.remove("mission_temp_script.py")

python_executor_tool = Tool(
    name="python_executor",
    description="Executes Python code. Use for EDA, training models, and data manipulation.",
    requires_approval=True, # HIGH RISK: REQUIRES HUMAN-IN-THE-LOOP FOR SECURITY
    func=python_executor_impl,
    schema=PythonExecutorSchema
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
