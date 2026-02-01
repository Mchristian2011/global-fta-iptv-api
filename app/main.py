# -----------------------------
# Import required modules
# -----------------------------
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.channels import router as channel_router
from app.models import Channel
from app.crud import add_channel

# -----------------------------
# LIFESPAN: STARTUP & SHUTDOWN
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    WHY THIS FUNCTION EXISTS:
    - Handles startup logic before the app is ready
    - Handles optional shutdown logic when the app stops
    """

    # 🔹 Startup logic: add sample channels to database
    sample_channels = [
        Channel(
            id="bbc_world",
            name="BBC World News",
            country="UK",
            language="English",
            category="News",
            stream_url="https://example.m3u8"
        ),
        Channel(
            id="france_24",
            name="France 24",
            country="France",
            language="French",
            category="News",
            stream_url="https://example.m3u8"
        ),
        Channel(
            id="dw_news",
            name="DW News",
            country="Germany",
            language="German",
            category="News",
            stream_url="https://example.m3u8"
        ),
    ]

    # 🔹 Persist each sample channel, skipping duplicates
    for channel in sample_channels:
        add_channel(channel)  # Interview gold: validates before persistence

    yield  # 🔹 App runs here

    # 🔻 Shutdown logic (optional)
    # e.g., close resources, stop background tasks

# -----------------------------
# CREATE FASTAPI APP INSTANCE
# -----------------------------
app = FastAPI(
    title="Global Free-To-Air IPTV API",
    version="1.0.0",
    description="Worldwide legal FTA TV channels API",
    lifespan=lifespan
)

# -----------------------------
# ROOT ENDPOINT
# -----------------------------
@app.get("/")
def root():
    """
    WHY THIS FUNCTION EXISTS:
    - Simple health check for the API
    - Confirms the service is running
    """
    return {"message": "Global Free-To-Air IPTV API is running"}

# -----------------------------
# INCLUDE ROUTERS
# -----------------------------
app.include_router(channel_router)
# WHY:
# - All /channels endpoints are registered
# - API key protection and filtering handled in router

# -----------------------------
# BACKGROUND STREAM HEALTH CHECK
# -----------------------------
import threading
from app.health_check import check_streams_forever

@app.on_event("startup")
def start_stream_checker():
    """
    WHY THIS FUNCTION EXISTS:
    - Starts a background thread to continuously check stream URLs
    - Ensures all streams remain valid while API runs
    """
    thread = threading.Thread(
        target=check_streams_forever,
        daemon=True  # 🔹 Thread won't block shutdown
    )
    thread.start()
