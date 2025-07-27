from fastapi import FastAPI
from agents import register_agents

app = FastAPI(title="PLUTO-JACKAL Core API")

@app.on_event("startup")
async def startup_event():
    register_agents()

@app.get("/")
async def root():
    return {"status": "PLUTO-JACKAL Core API running"}
