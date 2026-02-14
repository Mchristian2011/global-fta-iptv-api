from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.channel import Channel
from app.database import ChannelDB, SessionLocal


# -----------------------------
# Add a channel
# -----------------------------
def add_channel(channel: Channel):
    """
    PURPOSE:
    - Adds a new channel to the database
    - Prevents duplicate IDs
    - Uses defensive database handling
    """

    db = SessionLocal()

    try:
        # 🔍 Check if channel already exists
        existing = (
            db.query(ChannelDB)
            .filter(ChannelDB.id == channel.id)
            .first()
        )

        if existing:
            return  # Already exists, silently ignore

        # 🆕 Create new DB object
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

    except SQLAlchemyError:
        db.rollback()
        raise

    finally:
        db.close()


# -----------------------------
# Get all channels
# -----------------------------
def get_all_channels():
    """
    PURPOSE:
    - Returns all channels in the database
    """

    db = SessionLocal()

    try:
        return db.query(ChannelDB).all()
    finally:
        db.close()


# -----------------------------
# Get channels by country
# -----------------------------
def get_channels_by_country(country: str):
    """
    PURPOSE:
    - Filters channels by country
    - Case-insensitive match
    """

    db = SessionLocal()

    try:
        return (
            db.query(ChannelDB)
            .filter(ChannelDB.country.ilike(f"%{country}%"))
            .all()
        )
    finally:
        db.close()


# -----------------------------
# Get channels by language
# -----------------------------
def get_channels_by_language(language: str):
    """
    PURPOSE:
    - Filters channels by language
    - Case-insensitive match
    """

    db = SessionLocal()

    try:
        return (
            db.query(ChannelDB)
            .filter(ChannelDB.language.ilike(f"%{language}%"))
            .all()
        )
    finally:
        d
