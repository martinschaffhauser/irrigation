import sqlite3
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# custom imports
from api.operations.jobs import run_scheduled_script
from api.operations.database import init_db, read_sql_statement
from log_config import setup_logging


scheduler = BackgroundScheduler()

setup_logging()


def start_scheduler():
    scheduler.start()
    init_db()
    load_jobs_from_db()


def shutdown_scheduler():
    scheduler.shutdown()


def load_jobs_from_db():
    sql_statement = read_sql_statement("api/operations/sql_statements/get_jobs.sql")
    conn = sqlite3.connect("jobs.db")
    c = conn.cursor()
    # c.execute("SELECT * FROM jobs")
    c.execute(sql_statement)
    jobs = c.fetchall()
    for job in jobs:
        # here job description does not need to be passed to the schedule_job function -> see db fields
        schedule_job(job[0], job[2], job[3], job[4])
    conn.close()


def schedule_job(job_id, script_path, mqtt_args, cron):
    cron_parts = cron.split()
    if len(cron_parts) == 6:
        trigger = CronTrigger(
            second=cron_parts[0],
            minute=cron_parts[1],
            hour=cron_parts[2],
            day=cron_parts[3],
            month=cron_parts[4],
            day_of_week=cron_parts[5],
        )
    elif len(cron_parts) == 5:
        trigger = CronTrigger(
            minute=cron_parts[0],
            hour=cron_parts[1],
            day=cron_parts[2],
            month=cron_parts[3],
            day_of_week=cron_parts[4],
        )
    else:
        raise ValueError("Invalid cron expression: {}".format(cron))

    scheduler.add_job(
        run_scheduled_script, trigger, id=job_id, args=[script_path, mqtt_args]
    )


def log_scheduled_jobs():
    jobs = scheduler.get_jobs()
    for job in jobs:
        logging.info(f"SCHEDULED JOB: {job.id}, NEXT RUN TIME: {job.next_run_time}")
