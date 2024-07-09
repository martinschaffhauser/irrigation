from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os


router = APIRouter()
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.environ.get("API_DOC_USER", "admin")
    correct_password = os.environ.get("API_DOC_PASS", "secret")

    if (
        credentials.username == correct_username
        and credentials.password == correct_password
    ):
        return credentials.username
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


### CUSTOM DOCS URL ###
@router.get("/docs", include_in_schema=False)
async def custom_docs(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Docs")


### CUSTOM REDOC URL ###
@router.get("/redoc", include_in_schema=False)
async def custom_redoc(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="Custom Redoc")
