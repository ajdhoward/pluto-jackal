import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uuid, datetime
import uvicorn

app = FastAPI(title="PLUTO-JACKAL Orchestrator", version="0.1")

AGENTS = {
    "chronolog": "ChronoLog (Meta-Auditor)",
    "forgerunner": "ForgeRunner (IaC Engineer)",
    "protosmith": "ProtoSmith (Code Generator)",
    "roleweaver": "RoleWeaver (Org Designer)",
    "nexusbuilder": "NexusBuilder (App Orchestrator)",
    "tether": "Tether (API Integrator)",
    "sentineledge": "SentinelEdge (Security + Monitoring)"
}

class Task(BaseModel):
    agent: str
    objective: str
    context: dict = {}

TASK_LOG = []

@app.get("/")
def read_root():
    return {"message": "PLUTO-JACKAL Core API online.", "agents": AGENTS}

@app.post("/task")
def assign_task(task: Task):
    task_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()
    log_entry = {
        "task_id": task_id,
        "timestamp": timestamp,
        "agent": task.agent,
        "objective": task.objective,
        "context": task.context,
    }
    TASK_LOG.append(log_entry)
    return {"message": f"Task assigned to {AGENTS.get(task.agent)}", "task_id": task_id}

@app.get("/log")
def get_log():
    return {"task_log": TASK_LOG}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("pluto_jackal_api:app", host="0.0.0.0", port=port)
