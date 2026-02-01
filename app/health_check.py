import time
from app.validator import validate_stream
from app.database import SessionLocal, ChannelDB

def check_streams_forever(interval=300):
    """
    Periodically checks all streams and updates status
    """
    while True:
        db = SessionLocal()
        channels = db.query(ChannelDB).all()

        for channel in channels:
            channel.is_active = validate_stream(channel.stream_url)

        db.commit()
        db.close()
        time.sleep(interval)
