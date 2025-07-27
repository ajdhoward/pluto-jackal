# PLUTO-JACKAL Core
Core orchestration API for AcidWurx.

## Local Dev
python pluto_jackal_api.py
# or
uvicorn pluto_jackal_api:app --reload

## Railway
Use Dockerfile or railway.json; listen on $PORT.

## Render
Build: pip install -r requirements.txt
Start: uvicorn pluto_jackal_api:app --host 0.0.0.0 --port $PORT

Health: /healthz
