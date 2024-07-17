import logging
from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from api.operations.token_validation import validate_token
from api.routers.limiter import limiter
from log_config import setup_logging

setup_logging()

router = APIRouter()

# OAuth2 Password Bearer Token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/health", response_class=JSONResponse)
# @limiter.limit("10/second")
async def health_check(
    # token: str = Depends(oauth2_scheme),
):

    # validate_token()

    logging.info("health check endpoint hit")

    answer = {"message": "Irrigation API is running."}

    headers = {"Custom-Header": "Value"}
    return JSONResponse(content=answer, status_code=status.HTTP_200_OK, headers=headers)
