"""Utility functions for date conversion, file operations, and data parsing."""

import datetime
import json
import os
from datetime import datetime as dt
from typing import Any

from dateutil import tz


def save_to_json(data: Any, path: str) -> bool:
    """Save data to JSON file if SAVE env var is truthy. Returns True when saved."""
    should_save = os.getenv("SAVE") in {"1", "true", "True"}
    if not should_save:
        return False

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return True


def utc_to_est(utc_date_str: str | None) -> str | None:
    """Convert UTC datetime string to EST."""
    if not utc_date_str:
        return None

    utc_dt = datetime.datetime.fromisoformat(utc_date_str.replace("Z", "+00:00"))

    eastern = tz.gettz("America/New_York")
    est_dt = utc_dt.astimezone(eastern)

    return est_dt.strftime("%Y-%m-%d")


def parse_date(segment: str) -> str:
    """Parse date string from ticker segment."""
    year = 2000 + int(segment[:2])
    month_str = segment[2:5]
    day = int(segment[5:7])
    month = dt.strptime(month_str, "%b").month
    return f"{year:04d}-{month:02d}-{day:02d}"
