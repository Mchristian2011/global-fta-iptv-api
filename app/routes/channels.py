# -----------------------------
# Import required modules
# -----------------------------
from fastapi import APIRouter, Header, HTTPException, Depends
from typing import List
from app.models.channel import Channel  # Pydantic model for channel
from app.crud import get_channels_by_language, add_channel  # Import CRUD functions
import json  # To read channel data from file
import requests  # To validate external stream URLs

# -----------------------------
# API KEY CONFIGURATION
# -----------------------------
API_KEY = "my_secret_api_key"  # Hardcoded secret key (for demo)

def verify_api_key(x_api_key: str = Header(...)):
    """
    WHY THIS FUNCTION EXISTS:
    - Validates API key sent by client
    - If invalid, raises 401 Unauthorized
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# -----------------------------
# ROUTER CONFIGURATION
# -----------------------------
router = APIRouter(
    prefix="/channels",
    tags=["Channels"],
    dependencies=[Depends(verify_api_key)]  # 🔐 Protects ALL endpoints
)
# WHY:
# - All channel endpoints start with /channels
# - API key is required for every route automatically
# - No need to repeat Depends in each endpoint

# -----------------------------
# LOAD CHANNEL DATA
# -----------------------------
# Load once at startup to avoid re-reading file on every request
with open("data/channels.json", "r", encoding="utf-8") as file:
    channels_data = json.load(file)
    print(f"[DEBUG] Loaded {len(channels_data)} channels")

# -----------------------------
# ENDPOINT: GET ALL CHANNELS
# -----------------------------
@router.get("/", response_model=List[Channel])
def get_all_channels():
    """
    WHY THIS FUNCTION EXISTS:
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
    WHY THIS FUNCTION EXISTS:
    - Filters channels by country
    - Case-insensitive
    - Automatically protected by API key
    """
    country_lower = country.lower()

    # Filter channels that match the country
    return [
        channel for channel in channels_data
        if channel["country"].lower() == country_lower
    ]

# -----------------------------
# ENDPOINT: GET CHANNELS BY CATEGORY
# -----------------------------
@router.get("/category/{category}", response_model=List[Channel])
def get_channels_by_category(category: str):
    """
    WHY THIS FUNCTION EXISTS:
    - Returns channels filtered by category
    - Case-insensitive
    - Automatically protected by API key
    """
    category_lower = category.lower()

    # Filter channels that match the category
    return [
        channel for channel in channels_data
        if channel["category"].lower() == category_lower
    ]

# -----------------------------
# ENDPOINT: GET CHANNELS BY LANGUAGE
# -----------------------------
@router.get("/language/{language}", response_model=List[Channel])
def get_channels_by_language_endpoint(language: str):
    """
    WHY THIS FUNCTION EXISTS:
    - Returns channels filtered by language
    - Case-insensitive
    - Automatically protected by API key
    """
    # Call the CRUD function that queries the database for channels by language
    return get_channels_by_language(language)

# -----------------------------
# ENDPOINT: CREATE CHANNEL (VALIDATE STREAM URL FIRST)
# -----------------------------
@router.post(
    "/",
    response_model=Channel,
    dependencies=[Depends(verify_api_key)]
)
def create_channel(channel: Channel):
    """
    WHY THIS FUNCTION EXISTS:
    - Adds a new channel after validating stream URL
    - Interview gold: “We validate external resources before persistence.”
    """
    # Validate that the stream URL is reachable
    if not validate_stream(channel.stream_url):
        raise HTTPException(
            status_code=400,
            detail="Stream URL is not reachable"
        )

    # Add channel to the database
    add_channel(channel)

    return channel

# -----------------------------
# UTILITY: STREAM URL VALIDATION
# -----------------------------
def validate_stream(url: str) -> bool:
    """
    WHY THIS FUNCTION EXISTS:
    - Confirms that external stream URL is reachable
    - Prevents saving broken or invalid streams to DB
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False
