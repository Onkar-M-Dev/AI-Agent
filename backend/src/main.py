import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.db import init_db
from api.chat.routing import router as chat_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    init_db()
    logger.info("Database initialized")
    yield
    logger.info("Shutting down application...")


app = FastAPI(lifespan=lifespan)
app.include_router(chat_router, prefix="/api/chats")


API_KEY = os.environ.get("API_KEY")
MY_PROJECT = os.environ.get("MY_PROJECT") or "This is my Project"
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is required")


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai-platform"}

@app.get("/ready")
def ready():
    return {"ready": True}

@app.get("/")
def read_index():
    return {"hello":"world", "project_name":MY_PROJECT}
