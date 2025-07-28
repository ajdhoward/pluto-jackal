# queue.py
import uuid, datetime
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/queue", tags=["queue"])

class QueueTask(BaseModel):
    agent: str
    objective: str
    context: dict = {}

# In-memory for MVP; swap with SQLite/Supabase later
QUEUE = []

@router.post("")
def enqueue(task: QueueTask):
    item = {
        "id": str(uuid.uuid4()),
        "agent": task.agent,
        "objective": task.objective,
        "context": task.context,
        "status": "pending",
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    QUEUE.append(item)
    return {"id": item["id"]}

@router.get("/next")
def next_task():
    for t in QUEUE:
        if t["status"] == "pending":
            t["status"] = "in_progress"
            return t
    raise HTTPException(status_code=204, detail="No tasks")

@router.post("/{tid}/done")
def done(tid: str, result: dict):
    for t in QUEUE:
        if t["id"] == tid:
            t["status"] = "done"
            t["result"] = result
            t["finished_at"] = datetime.datetime.utcnow().isoformat()
            return {"ok": True}
    raise HTTPException(404, "Task not found")
