from fastapi import Header, HTTPException

API_KEYS = {
    "abc123",
    "test456"
}

async def verify_api_key(x_api_key: str = Header(...)):
    
    if x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )

    return x_api_key