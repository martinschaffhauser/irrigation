import logging
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

# custom imports
from api.routers.limiter import limiter
from api.operations.token_validation import validate_token
from api.operations import telnet
from log_config import setup_logging

setup_logging()

router = APIRouter(prefix="/monitor")


@router.get("/pumpesp")
async def get_telnet_output_1(
    # token: str = Depends(oauth2_scheme),
):
    # validate_token()

    logging.info(f"monitor/pumpesp endpoint was hit")
    headers = {"Custom-Header": "Value"}
    return JSONResponse(
        content=telnet.latest_output_pump_esp,
        status_code=status.HTTP_200_OK,
        headers=headers,
    )


@router.get("/thujaesp")
async def get_telnet_output_2(
    # token: str = Depends(oauth2_scheme),
):
    # validate_token()

    logging.info(f"monitor/thujaesp endpoint was hit")
    headers = {"Custom-Header": "Value"}
    return JSONResponse(
        content=telnet.latest_output_thuja_esp,
        status_code=status.HTTP_200_OK,
        headers=headers,
    )
