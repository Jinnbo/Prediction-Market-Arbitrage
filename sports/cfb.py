"""CFB Arbitrage Script"""

import asyncio
import logging
import time

from arbitrage import ArbitrageSportsCalculator
from kalshi import Kalshi
from normalize import NormalizeSportsMarket
from polymarket import Polymarket
from supabase import truncate_table

logger = logging.getLogger(__name__)


async def cfb():
    """CFB arbitrage calculator."""
    # Initialize clients
    cfb_kalshi = Kalshi(series_ticker="KXNCAAFGAME", market="cfb")
    cfb_polymarket = Polymarket(tag_id="100351", market="cfb")

    while True:
        script_start_time = time.time()

        # Fetch market data concurrently
        logger.info("Fetching market data from Kalshi and Polymarket concurrently...")
        markets_kalshi, markets_polymarket = await asyncio.gather(
            cfb_kalshi.get_market_data(), cfb_polymarket.get_market_data()
        )

        logger.info("Loaded %d Kalshi markets", len(markets_kalshi))
        logger.info("Loaded %d Polymarket markets", len(markets_polymarket))

        # Normalize markets
        logger.info("Normalizing markets...")
        cfb_normalizer = NormalizeSportsMarket(
            polymarket_markets=markets_polymarket,
            kalshi_markets=markets_kalshi,
            sport="cfb",
        )
        kalshi, polymarket = cfb_normalizer.normalize_markets()

        # Calculate Arbitrage
        logger.info("Calculating arbitrage opportunities...")
        arbitrage_calculator = ArbitrageSportsCalculator(
            kalshi_markets=kalshi,
            polymarket_markets=polymarket,
            sport="cfb",
        )
        truncate_table("cfb")
        arbitrage_calculator.calculate()

        script_elapsed_time = time.time() - script_start_time
        logger.info(
            "Script completed successfully in %.2f seconds", script_elapsed_time
        )
