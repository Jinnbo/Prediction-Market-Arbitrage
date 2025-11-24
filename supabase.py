"""Router for Supabase Edge Functions."""

import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
TABLE_WRITE_EDGE_FUNCTION_URL = os.getenv("TABLE_WRITE_EDGE_FUNCTION_URL")
headers = {"Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}"}


def write_sports_arbitrage_to_supabase(opportunity: dict[str, Any], sport: str) -> None:
    """Write sports arbitrage opportunity to Supabase via edge function."""
    try:
        response = requests.post(
            TABLE_WRITE_EDGE_FUNCTION_URL,
            json={**opportunity, "table": sport},
            headers=headers,
            timeout=30,
        )
        logger.info("Successfully wrote to Supabase: %s", response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Failed to write to Supabase: %s", e)


def truncate_table(table_name: str) -> None:
    """Truncate a table in Supabase via edge function."""
    truncate_table_url = os.getenv("TRUNCATE_TABLE_URL")
    try:
        response = requests.post(
            truncate_table_url,
            json={"table": table_name},
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        logger.info("Successfully truncated table: %s", table_name)
    except requests.exceptions.RequestException as e:
        logger.error("Failed to truncate table: %s", e)
