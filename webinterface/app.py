import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

### CUSTOM IMPORTS ###
from apimetadata import title, description, version
from api.routers.limiter import limiter
from api.routers.api_documentation_router import router as api_documentation_router
from api.routers.api_health_check_router import router as health_check_router
from api.routers.jobs_router import router as job_router
from api.routers.landing_page_router import router as landing_page_router
from api.routers.mqtt_scripts_router import router as mqtt_scripts_router
from api.routers.monitor_router import router as monitor_router
from api.operations.scheduler import start_scheduler, shutdown_scheduler
from api.operations.database import init_db

### LOAD ENV FILE ###
load_dotenv("../cred.env")


### INITIALIZE FASTAPI ###
app = FastAPI(
    title=title,
    version=version,
    description=description,
    docs_url=None,
    redoc_url=None,
)

### INCLUDE ALL ROUTES ###
app.include_router(landing_page_router)
app.include_router(api_documentation_router)
app.include_router(health_check_router)
app.include_router(job_router)
app.include_router(mqtt_scripts_router)
app.include_router(monitor_router)

### EVENT HANDLERS ###
app.add_event_handler("startup", start_scheduler)
app.add_event_handler("shutdown", shutdown_scheduler)

### RATE LIMITER ###
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

### ADD HTML STATIC ###
app.mount("/static", StaticFiles(directory="static"), name="static")

# ### CORS SETTINGS ###
# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     # Add more origins if needed
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: set correctly!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ADDING DEBUGGER
# import debugpy
# debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client()
