from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------
load_dotenv()  # <-- MUST be BEFORE os.getenv

# -----------------------------
# READ DATABASE URL FROM ENVIRONMENT
# -----------------------------
# WHY: Allows deployment to Render without hardcoding sensitive info
# Ensure DATABASE_URL uses the user with proper privileges (iptv_user)
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")  # Use in your API key validation

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing. Check your .env file.")

# -----------------------------
# CONNECT TO DATABASE
# -----------------------------
# Use connect_args to handle special cases if needed, e.g., SSL for production
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# -----------------------------
# BASE CLASS FOR MODELS
# -----------------------------
Base = declarative_base()

# -----------------------------
# CHANNEL TABLE MODEL
# -----------------------------
class ChannelDB(Base):
    __tablename__ = "channels"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    language = Column(String)
    category = Column(String)
    stream_url = Column(String)
    is_active = Column(Boolean, default=True)

# -----------------------------
# CREATE TABLES IF THEY DON'T EXIST
# -----------------------------
# Make sure the DB user has privileges on the public schema
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully or already exist")
except Exception as e:
    print("❌ Error creating tables:", e)
