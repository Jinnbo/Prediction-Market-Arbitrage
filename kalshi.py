import asyncio
import json
import logging
import time
from datetime import datetime

import aiohttp

logger = logging.getLogger(__name__)


class Kalshi:
    BASE_EVENTS_URL = "https://api.elections.kalshi.com/trade-api/v2/events"
    BASE_MARKETS_URL = "https://api.elections.kalshi.com/trade-api/v2/markets"

    def __init__(self, series_ticker):
        """Initialize Kalshi client with series ticker."""
        self.series_ticker = series_ticker
        self.status_filter = "open"
        self.market_data = []

    async def get_market_data(self):
        """Fetch and process market data from events."""
        start_time = time.time()
        logger.info(
            f"Starting Kalshi market data fetch for series: {self.series_ticker}"
        )

        async with aiohttp.ClientSession() as session:
            events = await self._fetch_events(session)
            logger.info(f"Fetched {len(events)} events from Kalshi")

            # Fetch markets for all events concurrently
            tasks = [
                self._fetch_markets_for_event(session, event["event_ticker"])
                for event in events
            ]
            markets_results = await asyncio.gather(*tasks, return_exceptions=True)

            results = []
            for i, event in enumerate(events):
                markets_result = markets_results[i]
                if isinstance(markets_result, Exception):
                    logger.error(
                        f"Failed to fetch markets for event {event['event_ticker']}: {markets_result}"
                    )
                    continue

                markets = markets_result
                event_title = event["title"]

                for m in markets:
                    ticker = m.get("ticker", "")
                    parts = ticker.split("-")

                    game_date = None
                    if len(parts) >= 2:
                        date_segment = parts[1][:7]
                        game_date = self._parse_date(date_segment)

                    results.append(
                        {
                            "event_title": event_title,
                            "market_ticker": ticker,
                            "game_date": game_date,
                            "yes_bid": m.get("yes_bid"),
                            "yes_ask": m.get("yes_ask"),
                            "no_bid": m.get("no_bid"),
                            "no_ask": m.get("no_ask"),
                        }
                    )

        elapsed_time = time.time() - start_time
        logger.info(
            f"Kalshi market data fetch completed in {elapsed_time:.2f} seconds. Loaded {len(results)} markets"
        )
        self.market_data = results
        self._save_to_json()
        return results

    async def _fetch_events(self, session):
        """Fetch open events from Kalshi API."""
        start_time = time.time()
        params = {"series_ticker": self.series_ticker, "status": self.status_filter}
        logger.debug(f"Fetching events from Kalshi with params: {params}")

        try:
            async with session.get(
                self.BASE_EVENTS_URL, params=params, timeout=30
            ) as response:
                response.raise_for_status()
                data = await response.json()
                elapsed_time = time.time() - start_time
                events = data.get("events", [])
                logger.debug(
                    f"Fetched {len(events)} events in {elapsed_time:.2f} seconds"
                )
                return events
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                f"Failed to fetch events from Kalshi after {elapsed_time:.2f} seconds: {e}"
            )
            raise

    async def _fetch_markets_for_event(self, session, event_ticker):
        """Fetch markets for a specific event."""

        start_time = time.time()
        params = {"event_ticker": event_ticker}
        logger.debug(f"Fetching markets for event: {event_ticker}")

        try:
            async with session.get(
                self.BASE_MARKETS_URL, params=params, timeout=30
            ) as response:
                response.raise_for_status()
                data = await response.json()
                elapsed_time = time.time() - start_time
                markets = data.get("markets", [])
                logger.debug(
                    f"Fetched {len(markets)} markets for event {event_ticker} in {elapsed_time:.2f} seconds"
                )
                return markets
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                f"Failed to fetch markets for event {event_ticker} after {elapsed_time:.2f} seconds: {e}"
            )
            raise

    def _parse_date(self, segment):
        """Parse date string from ticker segment."""
        year = 2000 + int(segment[:2])
        month_str = segment[2:5]
        day = int(segment[5:7])
        month = datetime.strptime(month_str, "%b").month
        return f"{year:04d}-{month:02d}-{day:02d}"

    def _save_to_json(self, path="data/nba_markets_kalshi.json"):
        """Save market data to JSON file."""
        with open(path, "w") as f:
            json.dump(self.market_data, f, indent=2)
