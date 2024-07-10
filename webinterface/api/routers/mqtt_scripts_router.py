import logging
import os
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

# Directory where the scripts are located
SCRIPT_DIR = "api/operations/mqtt_scripts"


@router.get("/mqttscripts", response_class=JSONResponse)
# @limiter.limit("10/second")
async def list_mqtt_scripts(
    # token: str = Depends(oauth2_scheme),
):

    # validate_token()

    logging.info("list mqtt scripts endpoint hit")

    files = [
        f for f in os.listdir(SCRIPT_DIR) if os.path.isfile(os.path.join(SCRIPT_DIR, f))
    ]

    headers = {"Custom-Header": "Value"}

    return JSONResponse(
        content={"scripts": files}, status_code=status.HTTP_200_OK, headers=headers
    )
