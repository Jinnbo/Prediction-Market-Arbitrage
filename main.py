import asyncio
import logging
import time

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

    logger.info("Loaded %d Kalshi markets", len(markets_kalshi))
    logger.info("Loaded %d Polymarket markets", len(markets_polymarket))

    # Normalize markets
    logger.info("Normalizing markets...")
    nba_normalizer = NormalizeNBAMarkets(markets_polymarket, markets_kalshi)
    kalshi, polymarket = nba_normalizer.normalize_markets()

    # Calculate Opportunity
    logger.info("Calculating arbitrage opportunities...")
    arbitrage_calculator = ArbitrageCalculator(market_1=polymarket, market_2=kalshi)
    arbitrage_calculator.calculate()

    script_elapsed_time = time.time() - script_start_time
    logger.info("Script completed successfully in %.2f seconds", script_elapsed_time)


if __name__ == "__main__":
    asyncio.run(main())
