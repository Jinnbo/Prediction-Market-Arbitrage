"""NBA Script"""

import asyncio
import logging
import time

from kalshi import Kalshi
from polymarket import Polymarket
from supabase import truncate_table

logger = logging.getLogger(__name__)


async def nhl():
    """NBA arbitrage calculator."""
    script_start_time = time.time()

    # Initialize clients
    nhl_kalshi = Kalshi(series_ticker="KXNHLGAME", market="nhl")

    # Fetch market data
    nhl_markets = await nhl_kalshi.get_market_data()
