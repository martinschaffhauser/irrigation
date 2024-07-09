import logging
import sqlite3

from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from api.operations.token_validation import validate_token
from api.operations.scheduler import scheduler, schedule_job, log_scheduled_jobs
from api.operations.scheduler import start_scheduler, shutdown_scheduler
from api.operations.database import read_sql_statement
from api.routers.limiter import limiter
from log_config import setup_logging

setup_logging()

router = APIRouter(prefix="/jobs")
scheduler = BackgroundScheduler()
scheduler.start()

# OAuth2 Password Bearer Token
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Job(BaseModel):
    id: str
    script_path: str
    cron: str


@router.post("/create")
# @limiter.limit("10/second")
def create_job(
    job: Job,
    # token: str = Depends(oauth2_scheme),
):
    # validate_token()
    logging.info("create job endpoint was hit")

    try:
        schedule_job(job.id, job.script_path, job.cron)
        sql_statement = read_sql_statement(
            "api/operations/sql_statements/create_job.sql"
        )
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()
        c.execute(
            sql_statement,
            (job.id, job.script_path, job.cron),
        )
        conn.commit()
        conn.close()
        return {"message": "Job created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete/{job_id}")
# @limiter.limit("10/second")
def delete_job(
    job_id: str,
    # token: str = Depends(oauth2_scheme),
):
    # validate_token()
    logging.info(f"delete job endpoint was hit with deletion of job id: {job_id}")

    try:
        # SHUTTING DOWN SCHEDULER TO THEN REMOVE JOB FROM DB
        # TODO: better implementation of removing jobs from scheduler; scheduler.remove_job(job_id) just does not work
        shutdown_scheduler()
        sql_statement = read_sql_statement(
            "api/operations/sql_statements/delete_job.sql"
        )
        conn = sqlite3.connect("jobs.db")
        c = conn.cursor()
        c.execute(sql_statement, (job_id,))
        conn.commit()
        conn.close()
        # RESTART SCHEDULER TO LOAD JOBS FROM DB
        start_scheduler()
        return {"message": "Job deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/get_db")
# @limiter.limit("10/second")
def list_jobs_db(
    # token: str = Depends(oauth2_scheme),
):
    # validate_token()
    logging.info("get jobs from db endpoint was hit")

    sql_statement = read_sql_statement("api/operations/sql_statements/get_jobs.sql")
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    # c.execute("SELECT * FROM jobs")
    c.execute(sql_statement)
    jobs = c.fetchall()
    conn.close()
    return {"jobs": jobs}


@router.get("/get_schedule")
# @limiter.limit("10/second")
def list_jobs_scheduler(
    # token: str = Depends(oauth2_scheme),
):
    # validate_token()
    logging.info("get jobs from schedule endpoint was hit")

    log_scheduled_jobs()
