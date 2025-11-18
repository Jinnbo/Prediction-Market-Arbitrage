import json
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

    def get_market_data(self):
        """Fetch and process market data from events."""

        events = self._fetch_events()
        results = []

        for event in events:
            event_ticker = event["event_ticker"]
            event_title = event["title"]

            markets = self._fetch_markets_for_event(event_ticker)

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
        response = requests.get(self.BASE_EVENTS_URL, params=params)
        response.raise_for_status()
        return response.json().get("events", [])

    def _fetch_markets_for_event(self, event_ticker):
        """Fetch markets for a specific event."""

        response = requests.get(
            self.BASE_MARKETS_URL, params={"event_ticker": event_ticker}
        )
        response.raise_for_status()
        return response.json().get("markets", [])

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
