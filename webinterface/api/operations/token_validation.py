from fastapi import HTTPException, status
import os


# Dependency for Token Validation
def validate_token(token: str):
    if token != os.environ.get("SECRET_TOKEN"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
