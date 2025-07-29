# wizard.py
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["wizard"])

# Dumb static steps for MVP; replace with GuideBuilder later
WIZARD_STEPS = [
    {
        "n": 1,
        "what": "Revoke leaked PATs",
        "how": "Open https://github.com/settings/personal-access-tokens and click Revoke.",
        "check": "Token gone from list.",
        "status": "pending",
    },
    {
        "n": 2,
        "what": "Create GitHub App",
        "how": "Go to https://github.com/settings/apps/new and fill fields as per instructions.",
        "check": "App ID visible, PEM downloaded.",
        "status": "pending",
    },
    {
        "n": 3,
        "what": "Add env vars to Railway",
        "how": "Railway → Variables → add GITHUB_APP_ID, etc.",
        "check": "Webhook ping returns 200.",
        "status": "pending",
    },
    {
        "n": 4,
        "what": "Start worker on VPS",
        "how": "ssh root@VPS → cd /opt/acidwurx/pluto-jackal/vps → docker compose up -d",
        "check": "docker logs show worker polling.",
        "status": "pending",
    },
]


def current_step():
    for s in WIZARD_STEPS:
        if s["status"] == "pending":
            return s
    return None


@router.get("/wizard", response_class=HTMLResponse)
async def wizard_page(request: Request):
    return templates.TemplateResponse("wizard.html", {"request": request})


@router.get("/wizard/state", response_class=HTMLResponse)
async def wizard_state(request: Request):
    step = current_step()
    return templates.TemplateResponse(
        "wizard_state.html", {"request": request, "step": step, "steps": WIZARD_STEPS}
    )


@router.post("/wizard/mark")
async def wizard_mark(n: int = Form(...), result: str = Form(...)):
    for s in WIZARD_STEPS:
        if s["n"] == n:
            s["status"] = "done" if result == "ok" else "blocked"
            break
    return HTMLResponse(status_code=204)
