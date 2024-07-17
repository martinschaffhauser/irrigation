import logging
import os
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from api.operations.token_validation import validate_token
from api.routers.limiter import limiter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from log_config import setup_logging


setup_logging()

router = APIRouter()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
# @limiter.limit("10/second")
async def get_landing_page(request: Request):
    # validate_token()

    # load env var (.env file was loaded by app.py)
    api_url = os.getenv("API_URL")

    return templates.TemplateResponse(
        "index.html", {"request": request, "api_url": api_url}
    )
