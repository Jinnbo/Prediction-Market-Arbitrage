import asyncio
import json

import arbitrage
from arbitrage import ArbitrageCalculator
from kalshi import Kalshi
from normalize_nba_markets import NormalizeNBAMarkets
from polymarket import Polymarket


async def main():
    # Kalshi
    nba_kalshi = Kalshi(series_ticker="KXNBAGAME")
    markets_kalshi = nba_kalshi.get_market_data()
    print("Loaded", len(markets_kalshi), "Kalshi markets")

    # Polymarket
    nba_polymarket = Polymarket(tag_id="745")
    markets_polymarket = await nba_polymarket.get_market_data()
    print("Loaded", len(markets_polymarket), "Polymarket markets")

    # Normalize markets
    nba_normalizer = NormalizeNBAMarkets(markets_polymarket, markets_kalshi)
    kalshi, polymarket = nba_normalizer.normalize_markets()

    # Calculate Opportunity
    arbitrageCalculator = ArbitrageCalculator(market_1=polymarket, market_2=kalshi)
    arbitrageCalculator.calculate()


if __name__ == "__main__":
    asyncio.run(main())
