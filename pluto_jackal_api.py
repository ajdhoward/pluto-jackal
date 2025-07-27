from fastapi import FastAPI

# Initialize the FastAPI app
app = FastAPI(
    title="Pluto Jackal API",
    description="API for Pluto Jackal project",
    version="1.0.0",
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to the Pluto Jackal API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/api/v1/test",
            "/docs"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "pluto-jackal"}

# Existing API routes (assuming you have something like this)
@app.get("/api/v1/test")
async def test_endpoint():
    return {"message": "API v1 is working"}

# Docs redirect if needed
@app.get("/docs")
async def docs_redirect():
    return {"message": "Visit /api/v1/docs for API documentation"}