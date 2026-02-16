"""FastAPI backend application."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import routes
from .routes import prediction, monitoring, response

# Lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage FastAPI lifespan."""
    logger.info("Starting CyberIntent-AI API")
    yield
    logger.info("Shutting down CyberIntent-AI API")


# Create FastAPI app
app = FastAPI(
    title="CyberIntent-AI API",
    description="AI-powered cybersecurity threat detection API",
    version="0.1.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(prediction.router, prefix="/api/predict", tags=["Prediction"])
app.include_router(monitoring.router, prefix="/api/monitor", tags=["Monitoring"])
app.include_router(response.router, prefix="/api/response", tags=["Response"])


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "message": "CyberIntent-AI API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "CyberIntent-AI"
    }


@app.get("/docs")
async def docs():
    """API documentation."""
    return {"docs": "Visit /docs for interactive documentation"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
