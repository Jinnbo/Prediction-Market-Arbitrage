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
    nhl_polymarket = Polymarket(tag_id="899", market="nhl")

    # Fetch market data
    markets_kalshi, markets_polymarket = await asyncio.gather(
        nhl_kalshi.get_market_data(), nhl_polymarket.get_market_data()
    )
