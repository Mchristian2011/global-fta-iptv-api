# -----------------------------
# Import BaseModel from Pydantic
# -----------------------------
# WHY:
# - Pydantic validates and documents API data automatically
from pydantic import BaseModel, Field, HttpUrl

# -----------------------------
# CHANNEL SCHEMA
# -----------------------------
class Channel(BaseModel):
    """
    WHY THIS CLASS EXISTS:
    - Defines what a Channel looks like
    - Used for documentation (Swagger UI)
    - Used for validation (ensures correct data types)
    """
    id: str               # Unique channel identifier
    name: str        # -----------------------------
# Import BaseModel and Field from Pydantic
# -----------------------------
# WHY:
# - BaseModel defines structured data models
# - Field allows metadata (examples, descriptions)
# - HttpUrl validates that stream_url is a real URL
from pydantic import BaseModel, Field, HttpUrl


# -----------------------------
# CHANNEL SCHEMA
# -----------------------------
class Channel(BaseModel):
    """
    WHY THIS CLASS EXISTS:
    - Defines what a Channel object looks like
    - Automatically validates data types
    - Generates Swagger documentation
    - Ensures API responses follow a strict structure
    """

    id: str = Field(
        ...,
        example="bbc-world-001",
        description="Unique channel identifier"
    )

    name: str = Field(
        ...,
        example="BBC World News",
        description="Official channel name"
    )

    country: str = Field(
        ...,
        example="United Kingdom",
        description="Country where the channel is based"
    )

    language: str = Field(
        ...,
        example="English",
        description="Primary broadcast language"
    )

    category: str = Field(
        ...,
        example="News",
        description="Channel category (News, Sports, Movies, etc.)"
    )

    stream_url: HttpUrl = Field(
        ...,
        example="https://example.com/stream.m3u8",
        description="Public streaming URL (must be valid HTTP/HTTPS)"
    )

    is_active: bool = Field(
        default=True,
        example=True,
        description="Indicates whether the stream is currently active"
    )
     # Channel name (e.g., BBC World)
    country: str          # Country (e.g., UK)
    language: str         # Language (e.g., English)
    category: str         # Category (News, Sports, Movies, etc.)
    stream_url: str       # Streaming URL
    is_active: bool = True  # Whether the stream is working (default True)
