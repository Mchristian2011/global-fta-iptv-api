import requests

def validate_stream(url: str) -> bool:
    """
    Checks if a stream URL is reachable.
    Returns True if valid, False if dead.
    """
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False
