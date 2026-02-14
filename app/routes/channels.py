# -----------------------------
# Import required modules
# -----------------------------
# WHY:
# - APIRouter organizes endpoints into modular components
# - Depends allows dependency injection (API key protection)
# - HTTPException handles API errors properly
from fastapi import Depends
from app.core.security import verify_api_key
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.channel import Channel
from app.crud import get_channels_by_language, add_channel
from app.core.auth import verify_api_key  # 🔐 Centralized security
import json
import requests


# -----------------------------
# ROUTER CONFIGURATION
# -----------------------------
router = APIRouter(
    prefix="/channels",
    tags=["Channels"],
    dependencies=[Depends(verify_api_key)]  # 🔐 Protects ALL endpoints
)

# WHY:
# - All routes start with /channels
# - API key verification applies automatically
# - Cleaner and DRY (Don’t Repeat Yourself)


# -----------------------------
# LOAD CHANNEL DATA (Temporary JSON Storage)
# -----------------------------
# WHY:
# - Loaded once at startup
# - Avoids reading file on every request
# - Good for demo version (not production database)
with open("data/channels.json", "r", encoding="utf-8") as file:
    channels_data = json.load(file)


# -----------------------------
# ENDPOINT: GET ALL CHANNELS
# -----------------------------




@router.get("/", dependencies=[Depends(verify_api_key)])
def get_all_channels():
    """
    PURPOSE:
    - Returns all FTA channels
    - Automatically protected by API key
    """
    return channels_data


# -----------------------------
# ENDPOINT: GET CHANNELS BY COUNTRY
# -----------------------------
@router.get("/country/{country}", response_model=List[Channel])
def get_channels_by_country(country: str):
    """
    PURPOSE:
    - Filters channels by country
    - Case-insensitive comparison
    """

    return [
        channel
        for channel in channels_data
        if channel["country"].lower() == country.lower()
    ]


# -----------------------------
# ENDPOINT: GET CHANNELS BY CATEGORY
# -----------------------------
@router.get("/category/{category}", response_model=List[Channel])
def get_channels_by_category(category: str):
    """
    PURPOSE:
    - Filters channels by category
    - Case-insensitive comparison
    """

    return [
        channel
        for channel in channels_data
        if channel["category"].lower() == category.lower()
    ]


# -----------------------------
# ENDPOINT: GET CHANNELS BY LANGUAGE (DB VERSION)
# -----------------------------
@router.get("/language/{language}", response_model=List[Channel])
def get_channels_by_language_endpoint(language: str):
    """
    PURPOSE:
    - Retrieves channels from database
    - Uses CRUD layer (clean architecture)
    """

    return get_channels_by_language(language)


# -----------------------------
# ENDPOINT: CREATE NEW CHANNEL
# -----------------------------
@router.post("/", response_model=Channel)
def create_channel(channel: Channel):
    """
    PURPOSE:
    - Adds a new channel
    - Validates external stream before saving
    - Demonstrates defensive programming
    """

    # Validate stream URL before saving
    if not validate_stream(channel.stream_url):
        raise HTTPException(
            status_code=400,
            detail="Stream URL is not reachable"
        )

    # Persist channel using CRUD layer
    add_channel(channel)

    return channel


# -----------------------------
# UTILITY: STREAM URL VALIDATION
# -----------------------------
def validate_stream(url: str) -> bool:
    """
    PURPOSE:
    - Sends HTTP HEAD request
    - Ensures stream is reachable
    - Prevents saving broken streams
    """

    try:
        response = requests.head(str(url), timeout=5)

        # Accept any 2xx success code
        return 200 <= response.status_code < 300

    except requests.RequestException:
        return False
