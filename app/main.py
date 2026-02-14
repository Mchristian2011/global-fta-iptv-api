from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.channels import router as channel_router
from app.models import Channel
from app.crud import add_channel, get_all_channels
from app.health_check import check_streams_forever
import threading

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Sample data
    sample_channels = [
        Channel(
            id="bbc_world",
            name="BBC World News",
            country="UK",
            language="English",
            category="News",
            stream_url="https://example.m3u8"
        )
    ]

    existing_ids = [c.id for c in get_all_channels()]
    for channel in sample_channels:
        if channel.id not in existing_ids:
            add_channel(channel)

    # Start background checker
    thread = threading.Thread(
        target=check_streams_forever,
        daemon=True
    )
    thread.start()

    yield

app = FastAPI(
    title="Global Free-To-Air IPTV API",
    version="1.0.0",
    description="Worldwide legal FTA TV channels API",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "API running"}

app.include_router(channel_router)
