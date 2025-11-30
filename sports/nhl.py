"""NHL Arbitrage Script"""

import asyncio
import logging
import time

from arbitrage import ArbitrageSportsCalculator
from kalshi import Kalshi
from normalize import NormalizeSportsMarket
from polymarket import Polymarket
from supabase_client import delete_by_sport

logger = logging.getLogger(__name__)


async def nhl():
    """NHL arbitrage calculator."""
    # Initialize clients
    nhl_kalshi = Kalshi(series_ticker="KXNHLGAME", market="nhl")
    nhl_polymarket = Polymarket(tag_id="899", market="nhl")

    while True:
        script_start_time = time.time()

        # Fetch market data
        markets_kalshi, markets_polymarket = await asyncio.gather(
            nhl_kalshi.get_market_data(), nhl_polymarket.get_market_data()
        )

        # Normalize markets
        nhl_normalizer = NormalizeSportsMarket(
            polymarket_markets=markets_polymarket,
            kalshi_markets=markets_kalshi,
            sport="nhl",
        )
        kalshi, polymarket = nhl_normalizer.normalize_markets()

        # Calcualte Arbitrage
        arbitrage_calculator = ArbitrageSportsCalculator(
            kalshi_markets=kalshi,
            polymarket_markets=polymarket,
            sport="nhl",
        )
        delete_by_sport("nhl")
        arbitrage_calculator.calculate()

        script_elapsed_time = time.time() - script_start_time
        logger.info(
            "Script completed successfully in %.2f seconds", script_elapsed_time
        )

        # Wait 30 seconds before next iteration to prevent rate limiting
        logger.info("Waiting 30 seconds before next iteration...")
        await asyncio.sleep(30)
