import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

import requests


class Kalshi:
    BASE_EVENTS_URL = "https://api.elections.kalshi.com/trade-api/v2/events"
    BASE_MARKETS_URL = "https://api.elections.kalshi.com/trade-api/v2/markets"

    def __init__(self, series_ticker):
        """Initialize Kalshi client with series ticker."""

        self.series_ticker = series_ticker
        self.status_filter = "open"
        self.market_data = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_market_data(self):
        """Fetch and process market data from events."""

        events = self._fetch_events()
        if not events:
            self.market_data = []
            return []

        results = []
        max_workers = min(16, len(events)) or 1
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_event = {
                executor.submit(
                    self._fetch_markets_for_event, event["event_ticker"]
                ): event
                for event in events
            }

            for future in as_completed(future_to_event):
                event = future_to_event[future]
                event_ticker = event["event_ticker"]
                event_title = event["title"]
                try:
                    markets = future.result()
                except Exception as exc:
                    self.logger.warning(
                        "Kalshi markets failed for %s: %s", event_ticker, exc
                    )
                    continue

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

        self.market_data = results
        return results

    def _fetch_events(self):
        """Fetch open events from Kalshi API."""

        params = {"series_ticker": self.series_ticker, "status": self.status_filter}
        start = time.perf_counter()
        response = requests.get(self.BASE_EVENTS_URL, params=params)
        response.raise_for_status()
        events = response.json().get("events", [])
        duration = time.perf_counter() - start
        self.logger.info(
            "Kalshi events fetched in %.2fs (series=%s, count=%d, params=%s)",
            duration,
            self.series_ticker,
            len(events),
            params,
        )
        return events

    def _fetch_markets_for_event(self, event_ticker):
        """Fetch markets for a specific event."""

        params = {"event_ticker": event_ticker}
        start = time.perf_counter()
        response = requests.get(self.BASE_MARKETS_URL, params=params)
        response.raise_for_status()
        markets = response.json().get("markets", [])
        duration = time.perf_counter() - start
        self.logger.info(
            "Kalshi markets fetched in %.2fs (event=%s, count=%d)",
            duration,
            event_ticker,
            len(markets),
        )
        return markets

    def _parse_date(self, segment):
        """Parse date string from ticker segment."""

        year = 2000 + int(segment[:2])
        month_str = segment[2:5]
        day = int(segment[5:7])
        month = datetime.strptime(month_str, "%b").month
        return f"{year:04d}-{month:02d}-{day:02d}"

    def _save_to_file(self, path="markets_kalshi.json"):
        """Save market data to JSON file."""

        with open(path, "w") as f:
            json.dump(self.market_data, f, indent=2)
        return path
