from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL (local Postgres)
DATABASE_URL = "postgresql+psycopg2://postgres:Ntimba%21%4012@localhost:5432/iptv_db"



# Connect to database
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base class for models
Base = declarative_base()

# Channel table
class ChannelDB(Base):
    __tablename__ = "channels"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
    language = Column(String)
    category = Column(String)
    stream_url = Column(String)
    is_active = Column(Boolean, default=True)

    # Create tables if not exist
Base.metadata.create_all(bind=engine)
