import asyncio
import json
import logging
import time

import arbitrage
from arbitrage import ArbitrageCalculator
from kalshi import Kalshi
from normalize_nba_markets import NormalizeNBAMarkets
from polymarket import Polymarket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def main():
    script_start_time = time.time()
    logger.info("Starting prediction market arbitrage script")

    # Initialize clients
    nba_kalshi = Kalshi(series_ticker="KXNBAGAME")
    nba_polymarket = Polymarket(tag_id="745")

    # Fetch market data concurrently
    logger.info("Fetching market data from Kalshi and Polymarket concurrently...")
    markets_kalshi, markets_polymarket = await asyncio.gather(
        nba_kalshi.get_market_data(), nba_polymarket.get_market_data()
    )

    logger.info(f"Loaded {len(markets_kalshi)} Kalshi markets")
    logger.info(f"Loaded {len(markets_polymarket)} Polymarket markets")

    # Normalize markets
    logger.info("Normalizing markets...")
    nba_normalizer = NormalizeNBAMarkets(markets_polymarket, markets_kalshi)
    kalshi, polymarket = nba_normalizer.normalize_markets()

    # Calculate Opportunity
    logger.info("Calculating arbitrage opportunities...")
    arbitrageCalculator = ArbitrageCalculator(market_1=polymarket, market_2=kalshi)
    arbitrageCalculator.calculate()

    script_elapsed_time = time.time() - script_start_time
    logger.info(f"Script completed successfully in {script_elapsed_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
