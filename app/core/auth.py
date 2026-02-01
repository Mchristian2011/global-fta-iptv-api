from fastapi import Header, HTTPException  # For reading headers and returning errors

# Define valid API keys
VALID_API_KEYS = {
    "FREE123": "free",  # Free tier
    "PRO456": "pro"     # Paid tier
}

# Dependency to check API key
def verify_api_key(x_api_key: str = Header(...)):
    """
    FastAPI dependency that checks if the client sent a valid API key.
    If invalid, it raises a 401 error.
    """
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key  # Return valid key
