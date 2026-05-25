from __future__ import annotations

import logging
import datetime as dt
from pathlib import Path

from apscheduler.schedulers.blocking import BlockingScheduler

from .job import run_model

LOGGER = logging.getLogger(__name__)


def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def build_scheduler(
    hour: int,
    minute: int,
    second: int,
    model_path: Path,
    log_path: Path,
    sample_input: list[list[float]] | None = None,
    interval_seconds: int | None = None,
    run_at: dt.datetime | None = None,
) -> BlockingScheduler:
    """Build a BlockingScheduler.

    Priority order:
    1. `run_at` for an exact one-time run.
    2. `interval_seconds` for repeated demo/testing runs.
    3. Daily cron schedule specified by hour/minute/second.
    """
    scheduler = BlockingScheduler()
    if run_at is not None:
        scheduler.add_job(
            run_model,
            "date",
            run_date=run_at,
            args=[model_path, log_path, sample_input],
            id="one-shot-model-job",
            replace_existing=True,
        )
    elif interval_seconds is not None:
        scheduler.add_job(
            run_model,
            "interval",
            seconds=interval_seconds,
            args=[model_path, log_path, sample_input],
            id="interval-model-job",
            replace_existing=True,
        )
    else:
        scheduler.add_job(
            run_model,
            "cron",
            hour=hour,
            minute=minute,
            second=second,
            args=[model_path, log_path, sample_input],
            id="daily-model-job",
            replace_existing=True,
        )
    return scheduler
