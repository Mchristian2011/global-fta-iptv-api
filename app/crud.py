from sqlalchemy.orm import Session
from app.models import Channel
from app.database import ChannelDB, SessionLocal

# -----------------------------
# Add a channel
# -----------------------------
def add_channel(channel: Channel):
    """
    Adds a new channel to the database.
    - Checks first to avoid duplicates (based on channel.id)
    """
    db = SessionLocal()

    # ✅ CHECK FIRST: prevent duplicate insert
    existing = db.query(ChannelDB).filter(ChannelDB.id == channel.id).first()
    if existing:
        db.close()
        return  # Channel already exists
    
    db_channel = ChannelDB(
        id=channel.id,
        name=channel.name,
        country=channel.country,
        language=channel.language,
        category=channel.category,
        stream_url=channel.stream_url,
        is_active=channel.is_active
    )
    db.add(db_channel)
    db.commit()
    db.close()


# -----------------------------
# Get all channels
# -----------------------------
def get_all_channels():
    """
    Returns all channels in the database.
    """
    db = SessionLocal()
    channels = db.query(ChannelDB).all()
    db.close()
    return channels


# -----------------------------
# Get channels by country
# -----------------------------
def get_channels_by_country(country: str):
    """
    Filters channels by country (case-insensitive)
    """
    db = SessionLocal()
    channels = db.query(ChannelDB)\
        .filter(ChannelDB.country.ilike(country))\
        .all()
    db.close()
    return channels


# -----------------------------
# Get channels by language
# -----------------------------
def get_channels_by_language(language: str):
    """
    Filters channels by language (case-insensitive)
    """
    db = SessionLocal()
    # Use ilike for case-insensitive matching
    channels = db.query(ChannelDB)\
        .filter(ChannelDB.language.ilike(language))\
        .all()
    db.close()
    return channels
