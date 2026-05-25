from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from apscheduler_ml_job.job import parse_sample_input, run_model
from apscheduler_ml_job.scheduler import build_scheduler, configure_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a scheduled ML model job with APScheduler.")
    parser.add_argument("--model-path", type=Path, default=Path("model.pkl"))
    parser.add_argument("--log-path", type=Path, default=Path("logs") / "model_runs.log")
    parser.add_argument("--hour", type=int, default=8)
    parser.add_argument("--minute", type=int, default=0)
    parser.add_argument("--second", type=int, default=0)
    parser.add_argument(
        "--interval-seconds",
        type=int,
        default=None,
        help="If set, schedule the job on an interval (seconds) for demo/testing.",
    )
    parser.add_argument(
        "--run-at",
        type=str,
        default=None,
        help="ISO timestamp for a one-time run, for example 2026-05-25T14:25:59.",
    )
    parser.add_argument(
        "--sample-input",
        type=str,
        default=None,
        help="Comma-separated feature row passed to model.predict, for example 1.0,2.0,3.0.",
    )
    return parser.parse_args()


def main() -> None:
    configure_logging()
    args = parse_args()
    sample_input = parse_sample_input(args.sample_input)

    run_at = None
    if args.run_at:
        run_at = dt.datetime.fromisoformat(args.run_at)

    run_model(args.model_path, args.log_path, sample_input)

    scheduler = build_scheduler(
        hour=args.hour,
        minute=args.minute,
        second=args.second,
        model_path=args.model_path,
        log_path=args.log_path,
        sample_input=sample_input,
        interval_seconds=args.interval_seconds,
        run_at=run_at,
    )
    scheduler.start()


if __name__ == "__main__":
    main()
