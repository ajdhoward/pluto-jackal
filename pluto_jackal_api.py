import os, uuid, datetime
from fastapi import FastAPI
from pydantic import BaseModel

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
def root():
    return {"message": "PLUTO-JACKAL Core API online.", "agents": AGENTS}

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/task")
def assign_task(task: Task):
    tid = str(uuid.uuid4())
    now = datetime.datetime.now().isoformat()
    entry = {
        "task_id": tid,
        "timestamp": now,
        "agent": task.agent,
        "objective": task.objective,
        "context": task.context,
    }
    TASK_LOG.append(entry)
    return {"message": f"Task assigned to {AGENTS.get(task.agent, task.agent)}", "task_id": tid}

@app.get("/log")
def get_log():
    return {"task_log": TASK_LOG}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("pluto_jackal_api:app", host="0.0.0.0", port=port)
