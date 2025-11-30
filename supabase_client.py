"""Supabase client for writing sports arbitrage opportunities."""

import logging
import os
from typing import Any

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize Supabase client
_supabase_client: Any | None = None


def _get_supabase_client() -> Any:
    """Get or create Supabase client instance."""
    global _supabase_client
    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment"
            )
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return _supabase_client


def write_sports_arbitrage_to_supabase(opportunities: list[dict[str, Any]]) -> None:
    """Write sports arbitrage opportunities to Supabase via client batch insert."""
    if not opportunities:
        logger.info("No opportunities to write to Supabase")
        return

    try:
        client = _get_supabase_client()
        response = client.table("sports").insert(opportunities).execute()
        logger.info(
            "Successfully wrote %d opportunities to Supabase", len(opportunities)
        )
    except Exception as e:
        logger.error("Failed to write opportunities to Supabase: %s", e)


def delete_by_sport(sport: str) -> None:
    """Delete all rows from sports table where sport field matches the given value."""
    try:
        client = _get_supabase_client()
        response = client.table("sports").delete().eq("sport", sport).execute()
        logger.info("Successfully deleted all rows for sport: %s", sport)
    except Exception as e:
        logger.error("Failed to delete rows for sport %s: %s", sport, e)
