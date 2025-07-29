# worker.py
import os
import time
import requests
import subprocess
from typing import Dict, Any

# --- Configuration ---
PLUTO_URL = os.getenv("PLUTO_URL")  # e.g., https://pluto-jackal-production.up.railway.app
PLUTO_TOKEN = os.getenv("PLUTO_TOKEN", "")  # Add auth if needed later
HEADERS = {"Authorization": f"Bearer {PLUTO_TOKEN}"} if PLUTO_TOKEN else {}
POLL_INTERVAL = 30  # seconds


def execute_task(task_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes a task received from the queue.
    This is a simplified example. You'll expand this logic.
    Context could contain 'command', 'script', 'params', etc.
    """
    print(f"[WORKER] Executing task ID: {task_data['id']}")
    print(f"[WORKER] Agent: {task_data['agent']}")
    print(f"[WORKER] Objective: {task_data['objective']}")
    print(f"[WORKER] Context: {task_data['context']}")

    context = task_data.get("context", {})
    result = {"status": "unknown", "output": "", "error": ""}

    try:
        # --- Handle ProtoSmith Script Execution ---
        if task_data["agent"] == "protosmith" and context.get("action") == "run_script":
            script_path = context.get("script_path")
            if script_path:
                print(f"[WORKER] Running script: {script_path}")
                proc = subprocess.Popen(
                    script_path,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = proc.communicate()
                result["status"] = "success" if proc.returncode == 0 else "failed"
                result["output"] = stdout
                result["error"] = stderr
                result["return_code"] = proc.returncode
            else:
                result["status"] = "failed"
                result["error"] = "Missing 'script_path' in context for protosmith."

        # --- Handle ForgeRunner Git Commit/Push ---
        elif task_data["agent"] == "forgerunner" and context.get("action") == "git_commit_push":
            message = context.get("commit_message", "Automated commit by Worker")
            try:
                subprocess.run(["git", "add", "."], check=True, cwd="/opt/acidwurx/your_repo")
                subprocess.run(["git", "commit", "-m", message], check=True, cwd="/opt/acidwurx/your_repo")
                subprocess.run(["git", "push"], check=True, cwd="/opt/acidwurx/your_repo")
                result["status"] = "success"
                result["output"] = "Git commit and push successful."
            except subprocess.CalledProcessError as e:
                result["status"] = "failed"
                result["error"] = f"Git command failed: {e}"

        # --- Handle Paperless Document Processing ---
        elif task_data["agent"] == "paperless" and context.get("action") == "process_document":
            doc_id = context.get("document_id")
            if doc_id:
                result["status"] = "success"
                result["output"] = f"Received task to process document ID {doc_id}. Processing logic goes here."
            else:
                result["status"] = "failed"
                result["error"] = "Missing 'document_id' in context for paperless agent."

        # --- Default Handler ---
        else:
            result["status"] = "skipped"
            result["output"] = f"No specific handler for agent '{task_data['agent']}' or action. Context: {context}"

    except Exception as e:
        result["status"] = "error"
        result["error"] = f"Exception during execution: {str(e)}"
        print(f"[WORKER] Error executing task {task_data['id']}: {e}")

    print(f"[WORKER] Task {task_data['id']} result: {result}")
    return result


def poll_and_execute():
    """Main worker loop."""
    if not PLUTO_URL:
        print("[ERROR] PLUTO_URL environment variable is not set.")
        return

    print(f"[WORKER] Starting worker. Polling {PLUTO_URL}/queue/next every {POLL_INTERVAL}s...")
    while True:
        try:
            response = requests.get(f"{PLUTO_URL}/queue/next", headers=HEADERS, timeout=10)
            if response.status_code == 200:
                task_data = response.json()
                print(f"[WORKER] Got task: {task_data['id']}")
                task_result = execute_task(task_data)

                # Report result back to PLUTO-JACKAL
                done_response = requests.post(
                    f"{PLUTO_URL}/queue/{task_data['id']}/done",
                    json={"result": task_result},
                    headers=HEADERS,
                    timeout=10,
                )
                if done_response.status_code == 200:
                    print(f"[WORKER] Successfully reported completion for task {task_data['id']}")
                else:
                    print(
                        f"[WORKER] Failed to report completion for task {task_data['id']}. "
                        f"Status: {done_response.status_code}, Text: {done_response.text}"
                    )

            elif response.status_code == 204:
                print("[WORKER] No tasks available.")
            else:
                print(f"[WORKER] Error fetching task. Status: {response.status_code}, Text: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"[WORKER] Network error while polling/communicating: {e}")
        except Exception as e:
            print(f"[WORKER] Unexpected error in worker loop: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    poll_and_execute()
