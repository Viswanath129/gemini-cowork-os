import uuid
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AgentRole(str, Enum):
    COORDINATOR = "Coordinator"
    STRATEGIC_ADVISOR = "StrategicAdvisor"
    RESEARCHER = "Researcher"
    DOCUMENTER = "Documenter"
    DATA_ANALYST = "DataAnalyst"
    BROWSER = "Browser"

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    description: str
    assigned_role: AgentRole
    dependencies: List[str] = Field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None
    artifacts: List[str] = Field(default_factory=list) # File paths

class ExecutionPlan(BaseModel):
    goal: str
    tasks: Dict[str, Task]
    
    def get_runnable_tasks(self) -> List[Task]:
        runnable = []
        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                # Check if all dependencies are COMPLETED
                deps_met = all(self.tasks[dep].status == TaskStatus.COMPLETED for dep in task.dependencies)
                if deps_met:
                    runnable.append(task)
        return runnable

class Artifact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    path: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
