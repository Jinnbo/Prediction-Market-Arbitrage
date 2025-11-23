import datetime
import json
from datetime import datetime as dt
from typing import Any

from dateutil import tz


def save_to_json(data: Any, path: str) -> None:
    """Save data to JSON file."""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


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


def calculate_nba_week(
    game_date: str, season_start_month: int = 10, season_start_day: int = 1
) -> int | None:
    """Calculate NBA week number from game date.

    Args:
        game_date: Date string in format YYYY-MM-DD
        season_start_month: Month when NBA season starts (default: 10 for October)
        season_start_day: Day when NBA season starts (default: 1)

    Returns:
        Week number (1-based) or None if date is invalid
    """
    if not game_date:
        return None

    try:
        game_dt = dt.strptime(game_date, "%Y-%m-%d")
        # Determine season year (season year is the later year, e.g., 2025-2026 season = 2026)
        if game_dt.month >= season_start_month:
            season_year = game_dt.year + 1
            season_start = dt(game_dt.year, season_start_month, season_start_day)
        else:
            season_year = game_dt.year
            season_start = dt(game_dt.year - 1, season_start_month, season_start_day)

        # Calculate days since season start
        days_diff = (game_dt - season_start).days

        # Calculate week (1-based, each week is 7 days)
        week = (days_diff // 7) + 1

        return max(1, week)  # Ensure week is at least 1
    except (ValueError, TypeError):
        return None
