# pluto_jackal_api.py
import os
import uuid
import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import json

app = FastAPI(title="PLUTO-JACKAL Orchestrator", version="0.2") # Bump version

# --- Agent Definitions ---
AGENTS = {
    "chronolog": "ChronoLog (Meta-Auditor)",
    "forgerunner": "ForgeRunner (IaC Engineer)",
    "protosmith": "ProtoSmith (Code Generator)",
    "roleweaver": "RoleWeaver (Org Designer)",
    "nexusbuilder": "NexusBuilder (App Orchestrator)",
    "tether": "Tether (API Integrator)",
    "sentineledge": "SentinelEdge (Security + Monitoring)",
    # Add more as needed
}

# --- Database Setup ---
DATABASE_FILE = "tasks.db"

def init_db():
    """Creates the tasks table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            agent TEXT NOT NULL,
            objective TEXT NOT NULL,
            context TEXT NOT NULL, -- Store as JSON string
            status TEXT NOT NULL DEFAULT 'pending',
            result TEXT, -- Store as JSON string
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# --- Pydantic Models ---
class Task(BaseModel):
    agent: str
    objective: str
    context: dict = {}

class QueueItem(BaseModel):
    id: str
    agent: str
    objective: str
    context: dict # Stored as JSON string in DB
    status: str = "pending"
    result: Optional[dict] = None
    created_at: str
    updated_at: str

class TaskResult(BaseModel):
    result: dict

# --- API Endpoints ---

@app.get("/")
def root():
    return {"message": "PLUTO-JACKAL Core API online.", "agents": AGENTS, "version": "0.2"}

@app.get("/healthz")
def healthz():
    return {"ok": True}

# Existing endpoint to log a task (adds to queue)
@app.post("/task")
def assign_task(task: Task):
    task_id = str(uuid.uuid4())
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    context_json = json.dumps(task.context) # Serialize context

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (id, agent, objective, context, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (task_id, task.agent, task.objective, context_json, 'pending', now, now))
    conn.commit()
    conn.close()

    return {"message": f"Task assigned to {AGENTS.get(task.agent, task.agent)}", "task_id": task_id}

# --- New Queue Endpoints ---

@app.post("/queue") # Alias for /task, or can be used directly
def enqueue(task: Task):
    # Reuse the logic from assign_task
    return assign_task(task)

@app.get("/queue/next")
def dequeue():
    """Get the next pending task and mark it as in_progress."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    # Use a transaction to ensure atomicity
    cursor.execute("BEGIN IMMEDIATE")
    cursor.execute('''
        SELECT id, agent, objective, context, status, result, created_at, updated_at
        FROM tasks
        WHERE status = 'pending'
        ORDER BY created_at ASC
        LIMIT 1
    ''')
    row = cursor.fetchone()
    if row:
        # Mark task as in_progress
        task_id = row[0]
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        cursor.execute('''
            UPDATE tasks
            SET status = 'in_progress', updated_at = ?
            WHERE id = ?
        ''', (now, task_id))
        conn.commit()
        conn.close()

        # Deserialize context
        context_dict = json.loads(row[3]) if row[3] else {}
        result_dict = json.loads(row[5]) if row[5] else None

        queue_item = QueueItem(
            id=row[0], agent=row[1], objective=row[2], context=context_dict,
            status='in_progress', result=result_dict, created_at=row[6], updated_at=now
        )
        return queue_item.dict() # Return as dict for JSON serialization
    else:
        conn.close()
        raise HTTPException(status_code=204, detail="No pending tasks")

@app.post("/queue/{task_id}/done")
def mark_done(task_id: str, task_result: TaskResult):
    """Mark a task as done with its result."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
    exists = cursor.fetchone()
    if not exists:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")

    result_json = json.dumps(task_result.result) # Serialize result
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    cursor.execute('''
        UPDATE tasks
        SET status = 'done', result = ?, updated_at = ?
        WHERE id = ?
    ''', (result_json, now, task_id))
    conn.commit()
    conn.close()
    return {"ok": True, "message": f"Task {task_id} marked as done."}

# Optional: Get task log/status
@app.get("/log")
def get_log():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, agent, objective, context, status, result, created_at, updated_at
        FROM tasks
        ORDER BY created_at DESC
        LIMIT 100 -- Limit for performance
    ''')
    rows = cursor.fetchall()
    conn.close()

    log_entries = []
    for row in rows:
        context_dict = json.loads(row[3]) if row[3] else {}
        result_dict = json.loads(row[5]) if row[5] else None
        entry = {
            "id": row[0],
            "agent": row[1],
            "objective": row[2],
            "context": context_dict,
            "status": row[4],
            "result": result_dict,
            "created_at": row[6],
            "updated_at": row[7],
        }
        log_entries.append(entry)

    return {"task_log": log_entries}


# --- Main Execution ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    print(f"Starting PLUTO-JACKAL API on port {port}...")
    uvicorn.run("pluto_jackal_api:app", host="0.0.0.0", port=port, reload=False) # Disable reload for production