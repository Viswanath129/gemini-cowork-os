from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import asyncio

from backend.app.core.orchestrator import Orchestrator

app = FastAPI(
    title="Gemini Cowork API",
    description="Autonomous Knowledge-Work Operating System",
    version="0.1.0"
)

orchestrator = Orchestrator()

class GoalRequest(BaseModel):
    prompt: str

class GoalResponse(BaseModel):
    message: str
    job_id: str

@app.post("/api/v1/goals", response_model=GoalResponse)
async def create_goal(request: GoalRequest, background_tasks: BackgroundTasks):
    """
    Accepts a high-level goal from the UI, starts the asynchronous execution engine.
    """
    # In a full system, we generate a UUID and save state to DB
    job_id = "job-1234" 
    
    # Run the orchestrator in the background so the HTTP request doesn't hang
    background_tasks.add_task(orchestrator.submit_goal, request.prompt)
    
    return GoalResponse(message="Goal received and execution DAG generated.", job_id=job_id)

@app.get("/api/v1/goals/{job_id}/status")
async def get_goal_status(job_id: str):
    """
    Returns the current graph state: which tasks are pending, running, awaiting approval.
    """
    return {"job_id": job_id, "status": "IN_PROGRESS", "active_agents": ["Researcher"]}

@app.post("/api/v1/approvals/{task_id}")
async def approve_task(task_id: str):
    """
    Human-in-the-loop endpoint. Resumes a paused Task DAG that hit a secure tool block.
    """
    return {"message": f"Task {task_id} approved. Resuming execution."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
