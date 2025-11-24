"""NBA Script"""

import asyncio
import logging
import time

from arbitrage import ArbitrageNBACalculator
from kalshi import Kalshi
from normalize import NormalizeNBAMarkets
from polymarket import Polymarket
from supabase import truncate_table

logger = logging.getLogger(__name__)


async def nba():
    """NBA arbitrage calculator."""
    script_start_time = time.time()

    # Initialize clients
    nba_kalshi = Kalshi(series_ticker="KXNBAGAME")
    nba_polymarket = Polymarket(tag_id="745")

    # while True:

    # Fetch market data concurrently
    logger.info("Fetching market data from Kalshi and Polymarket concurrently...")
    markets_kalshi, markets_polymarket = await asyncio.gather(
        nba_kalshi.get_market_data(), nba_polymarket.get_market_data()
    )

    logger.info("Loaded %d Kalshi markets", len(markets_kalshi))
    logger.info("Loaded %d Polymarket markets", len(markets_polymarket))

    # Normalize markets
    logger.info("Normalizing markets...")
    nba_normalizer = NormalizeNBAMarkets(markets_polymarket, markets_kalshi)
    kalshi, polymarket = nba_normalizer.normalize_markets()

    # Calculate Opportunity
    logger.info("Calculating arbitrage opportunities...")
    arbitrage_calculator = ArbitrageNBACalculator(market_1=polymarket, market_2=kalshi)
    truncate_table("nba")
    arbitrage_calculator.calculate()

    script_elapsed_time = time.time() - script_start_time
    logger.info("Script completed successfully in %.2f seconds", script_elapsed_time)
