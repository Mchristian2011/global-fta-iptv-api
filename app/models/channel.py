# Import BaseModel from Pydantic
# WHY:
# - Pydantic validates and documents API data automatically
from pydantic import BaseModel

# Channel schema
class Channel(BaseModel):
    """
    WHY THIS CLASS EXISTS:
    - Defines what a Channel looks like
    - Used for documentation (Swagger)
    - Used for validation (correct data types)
    """
    id: str
    name: str        # Channel name (e.g. BBC World)
    country: str     # Country (e.g. UK)
    language: str    # Language (e.g. English)
    category: str    # News, Sports, Movies
    stream_url: str  # Streaming URL
    is_active: bool = True  # Whether stream is working
