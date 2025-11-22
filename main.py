import asyncio
import logging
import time

from arbitrage import ArbitrageCalculator
from kalshi import Kalshi
from normalize_nba_markets import NormalizeNBAMarkets
from polymarket import Polymarket

logger = logging.getLogger("arbitrage-runner")


async def main():
    run_start = time.perf_counter()
    # Kalshi
    nba_kalshi = Kalshi(series_ticker="KXNBAGAME")

    # Polymarket
    nba_polymarket = Polymarket(tag_id="745")

    kalshi_task = asyncio.to_thread(nba_kalshi.get_market_data)
    polymarket_task = asyncio.create_task(nba_polymarket.get_market_data())
    markets_kalshi, markets_polymarket = await asyncio.gather(
        kalshi_task, polymarket_task
    )

    print("Loaded", len(markets_kalshi), "Kalshi markets")
    print("Loaded", len(markets_polymarket), "Polymarket markets")

    # Normalize markets
    nba_normalizer = NormalizeNBAMarkets(markets_polymarket, markets_kalshi)
    kalshi, polymarket = nba_normalizer.normalize_markets()

    # Calculate Opportunity
    arbitrageCalculator = ArbitrageCalculator(market_1=polymarket, market_2=kalshi)
    arbitrageCalculator.calculate()
    total_duration = time.perf_counter() - run_start
    logger.info("Full run completed in %.2fs", total_duration)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    asyncio.run(main())
