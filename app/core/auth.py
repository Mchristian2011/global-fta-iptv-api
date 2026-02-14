# app/core/security.py

import os
from fastapi import Header, HTTPException

# ---------------------------------------
# LOAD API KEYS FROM ENVIRONMENT
# ---------------------------------------
FREE_KEY = os.getenv("FREE_API_KEY")
PRO_KEY = os.getenv("PRO_API_KEY")

VALID_API_KEYS = {
    FREE_KEY: "free",
    PRO_KEY: "pro"
}

# ---------------------------------------
# DEPENDENCY FUNCTION
# ---------------------------------------
def verify_api_key(x_api_key: str = Header(None)):
    """
    PURPOSE:
    - Extracts X-API-Key header
    - Validates access
    - Returns subscription tier
    """

    if not x_api_key or x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )

    return VALID_API_KEYS[x_api_key]
