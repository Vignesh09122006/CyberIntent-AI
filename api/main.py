from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.prediction import router as prediction_router


app = FastAPI(
    title="CyberIntent-AI API",
    description="API for predictive cybersecurity risk scoring",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(prediction_router)
