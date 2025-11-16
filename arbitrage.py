import asyncio

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
    normalizer = NormalizeNBAMarkets(markets_polymarket, markets_kalshi)
    normalizer.normalize_markets()


if __name__ == "__main__":
    asyncio.run(main())
