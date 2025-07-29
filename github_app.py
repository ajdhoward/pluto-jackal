# github_app.py
import os
import hmac
import hashlib
import time
import json
import base64
import jwt
import requests
from fastapi import APIRouter, Request, HTTPException, Header

router = APIRouter(prefix="/github", tags=["github"])

WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY_B64 = os.getenv("GITHUB_APP_PRIVATE_KEY_B64")

if not (WEBHOOK_SECRET and APP_ID and PRIVATE_KEY_B64):
    print("⚠️ Missing GitHub env vars; webhook will fail until set.")

PRIVATE_KEY = base64.b64decode(PRIVATE_KEY_B64).decode() if PRIVATE_KEY_B64 else None


def verify_sig(payload: bytes, signature: str | None):
    if not WEBHOOK_SECRET:
        raise HTTPException(500, "No webhook secret configured")
    mac = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    if not signature or not hmac.compare_digest(expected, signature):
        raise HTTPException(401, "Invalid signature")


def make_app_jwt():
    now = int(time.time())
    payload = {"iat": now - 60, "exp": now + 540, "iss": APP_ID}
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")


def get_install_token(installation_id: int):
    token = make_app_jwt()
    r = requests.post(
        f"https://api.github.com/app/installations/{installation_id}/access_tokens",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        json={},
    )
    r.raise_for_status()
    return r.json()["token"]


@router.post("/webhook")
async def webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None),
):
    raw = await request.body()
    verify_sig(raw, x_hub_signature_256)
    event = json.loads(raw)

    # Minimal example: enqueue on push
    if x_github_event == "push":
        from queue import enqueue, QueueTask

        enqueue(
            QueueTask(
                agent="protosmith",
                objective=f"Process push on {event['repository']['full_name']}",
                context={"ref": event.get("ref"), "head": event.get("after")},
            )
        )
    return {"ok": True}
