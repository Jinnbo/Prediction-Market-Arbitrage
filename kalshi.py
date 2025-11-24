"""Kalshi API client for fetching prediction market data."""

import asyncio
import logging
import time
from typing import Any

import aiohttp

from utils import parse_date, save_to_json

logger = logging.getLogger(__name__)


class Kalshi:
    """Kalshi Client"""

    BASE_EVENTS_URL = "https://api.elections.kalshi.com/trade-api/v2/events"
    BASE_MARKETS_URL = "https://api.elections.kalshi.com/trade-api/v2/markets"

    def __init__(self, series_ticker: str, market: str) -> None:
        """Initialize Kalshi client with series ticker."""
        self.series_ticker = series_ticker
        self.status_filter = "open"
        self.market_data = []
        self.market = market

    async def get_market_data(self) -> list[dict[str, Any]]:
        """Fetch and process market data from events."""
        start_time = time.time()
        logger.info(
            "Starting Kalshi market data fetch for series: %s", self.series_ticker
        )

        async with aiohttp.ClientSession() as session:
            events = await self._fetch_events(session)
            logger.info("Fetched %d events from Kalshi", len(events))

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
                        "Failed to fetch markets for event %s: %s",
                        event["event_ticker"],
                        markets_result,
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
                        game_date = parse_date(date_segment)

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
            "Kalshi market data fetch completed in %.2f seconds. Loaded %d markets",
            elapsed_time,
            len(results),
        )
        self.market_data = results
        save_to_json(self.market_data, f"data/{self.market}_markets_kalshi.json")
        return results

    async def _fetch_events(
        self, session: aiohttp.ClientSession
    ) -> list[dict[str, Any]]:
        """Fetch open events from Kalshi API."""
        start_time = time.time()
        params = {"series_ticker": self.series_ticker, "status": self.status_filter}
        logger.debug("Fetching events from Kalshi with params: %s", params)

        try:
            async with session.get(
                self.BASE_EVENTS_URL, params=params, timeout=30
            ) as response:
                response.raise_for_status()
                data = await response.json()
                elapsed_time = time.time() - start_time
                events = data.get("events", [])
                logger.debug(
                    "Fetched %d events in %.2f seconds", len(events), elapsed_time
                )
                return events
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "Failed to fetch events from Kalshi after %.2f seconds: %s",
                elapsed_time,
                e,
            )
            raise

    async def _fetch_markets_for_event(
        self, session: aiohttp.ClientSession, event_ticker: str
    ) -> list[dict[str, Any]]:
        """Fetch markets for a specific event."""

        start_time = time.time()
        params = {"event_ticker": event_ticker}
        logger.debug("Fetching markets for event: %s", event_ticker)

        try:
            async with session.get(
                self.BASE_MARKETS_URL, params=params, timeout=30
            ) as response:
                response.raise_for_status()
                data = await response.json()
                elapsed_time = time.time() - start_time
                markets = data.get("markets", [])
                logger.debug(
                    "Fetched %d markets for event %s in %.2f seconds",
                    len(markets),
                    event_ticker,
                    elapsed_time,
                )
                return markets
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "Failed to fetch markets for event %s after %.2f seconds: %s",
                event_ticker,
                elapsed_time,
                e,
            )
            raise
