"""CS2 Arbitrage Script"""

import asyncio
import logging
import time

from arbitrage import ArbitrageSportsCalculator
from kalshi import Kalshi
from normalize import NormalizeSportsMarket
from polymarket import Polymarket
from supabase_client import delete_by_sport

logger = logging.getLogger(__name__)


async def cs2():
    """CS2 arbitrage calculator."""
    # Initialize clients
    cs2_kalshi = Kalshi(series_ticker="KXCSGOGAME", market="cs2")
    cs2_polymarket = Polymarket(tag_id="100780", market="cs2")

    while True:
        script_start_time = time.time()

        # Fetch market data concurrently
        logger.info("Fetching market data from Kalshi and Polymarket concurrently...")
        markets_kalshi, markets_polymarket = await asyncio.gather(
            cs2_kalshi.get_market_data(), cs2_polymarket.get_market_data()
        )

        logger.info("Loaded %d Kalshi markets", len(markets_kalshi))
        logger.info("Loaded %d Polymarket markets", len(markets_polymarket))

        # Normalize markets
        logger.info("Normalizing markets...")
        cs2_normalizer = NormalizeSportsMarket(
            polymarket_markets=markets_polymarket,
            kalshi_markets=markets_kalshi,
            sport="cs2",
        )
        kalshi, polymarket = cs2_normalizer.normalize_markets()

        # Calculate Arbitrage
        logger.info("Calculating arbitrage opportunities...")
        arbitrage_calculator = ArbitrageSportsCalculator(
            kalshi_markets=kalshi,
            polymarket_markets=polymarket,
            sport="cs2",
        )
        delete_by_sport("cs2")
        arbitrage_calculator.calculate()

        script_elapsed_time = time.time() - script_start_time
        logger.info(
            "Script completed successfully in %.2f seconds", script_elapsed_time
        )

        # Wait 30 seconds before next iteration to prevent rate limiting
        logger.info("Waiting 30 seconds before next iteration...")
        await asyncio.sleep(30)
