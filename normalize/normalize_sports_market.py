"""Normalizes sports market data from different prediction market platforms."""

import hashlib
import os
from collections import defaultdict
from typing import Any

from utils import save_to_json

from .constants import (
    CFB_KALSHI_BASE_URL,
    CFB_TEAM_MAPPING,
    CS2_KALSHI_BASE_URL,
    CS2_TEAM_MAPPING,
    NBA_KALSHI_BASE_URL,
    NBA_TEAM_MAPPING,
    NFL_KALSHI_BASE_URL,
    NFL_TEAM_MAPPING,
    NHL_KALSHI_BASE_URL,
    NHL_TEAM_MAPPING,
    POLYMARKET_URL,
)

SPORT_CONFIG: dict[str, dict[str, Any]] = {
    "nba": {
        "team_map": NBA_TEAM_MAPPING,
        "kalshi_url": NBA_KALSHI_BASE_URL,
        "polymarket_url": POLYMARKET_URL,
        "output_prefix": "nba",
    },
    "nhl": {
        "team_map": NHL_TEAM_MAPPING,
        "kalshi_url": NHL_KALSHI_BASE_URL,
        "polymarket_url": POLYMARKET_URL,
        "output_prefix": "nhl",
    },
    "nfl": {
        "team_map": NFL_TEAM_MAPPING,
        "kalshi_url": NFL_KALSHI_BASE_URL,
        "polymarket_url": POLYMARKET_URL,
        "output_prefix": "nfl",
    },
    "cfb": {
        "team_map": CFB_TEAM_MAPPING,
        "kalshi_url": CFB_KALSHI_BASE_URL,
        "polymarket_url": POLYMARKET_URL,
        "output_prefix": "cfb",
    },
    "cs2": {
        "team_map": CS2_TEAM_MAPPING,
        "kalshi_url": CS2_KALSHI_BASE_URL,
        "polymarket_url": POLYMARKET_URL,
        "output_prefix": "cs2",
    },
}


class NormalizeSportsMarket:
    """Normalizes sports market data from different prediction market platforms."""

    def __init__(
        self,
        polymarket_markets: list[dict[str, Any]],
        kalshi_markets: list[dict[str, Any]],
        sport: str,
    ) -> None:
        """Initialize normalizer with Polymarket and Kalshi market data."""
        self.polymarket_markets = polymarket_markets
        self.kalshi_markets = kalshi_markets
        self.sport = sport
        config = SPORT_CONFIG[sport]
        self.team_name_map = config["team_map"]
        self.kalshi_base_url = config["kalshi_url"]
        self.polymarket_base_url = config["polymarket_url"]
        self.output_prefix = config.get("output_prefix", sport)

    def normalize_markets(
        self, output_dir: str = "data", save: bool = True
    ) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
        """Normalize and optionally save market data from both platforms."""
        os.makedirs(output_dir, exist_ok=True)
        normalized_kalshi = self._normalize_kalshi_markets()
        normalized_polymarket = self._normalize_polymarket_markets()

        if save:
            save_to_json(
                normalized_kalshi,
                path=os.path.join(
                    output_dir, f"{self.output_prefix}_markets_kalshi_normalized.json"
                ),
            )
            save_to_json(
                normalized_polymarket,
                path=os.path.join(
                    output_dir,
                    f"{self.output_prefix}_markets_polymarket_normalized.json",
                ),
            )

        return normalized_kalshi, normalized_polymarket

    def _normalize_kalshi_markets(self) -> dict[str, dict[str, Any]]:
        """Normalize Kalshi market data to standard format."""
        grouped_markets = defaultdict(list)
        for market in self.kalshi_markets:
            key = (market["event_title"], market["game_date"])
            grouped_markets[key].append(market)

        normalized = []

        for (_, game_date), markets in grouped_markets.items():
            if len(markets) != 2:
                continue

            teams = {}
            for market in markets:
                ticker = market["market_ticker"]
                team_abbr = ticker.split("-")[-1] if "-" in ticker else None

                if team_abbr and team_abbr in self.team_name_map:
                    team_name = self.team_name_map[team_abbr]
                    teams[team_abbr] = {"name": team_name, "market": market}

            if len(teams) != 2:
                continue

            team_list = sorted(teams.values(), key=lambda x: x["name"])
            team1 = team_list[0]
            team2 = team_list[1]

            team1_buy = (
                team1["market"]["yes_ask"] / 100.0
                if team1["market"]["yes_ask"] is not None
                else None
            )
            team2_buy = (
                team2["market"]["yes_ask"] / 100.0
                if team2["market"]["yes_ask"] is not None
                else None
            )

            question = " vs ".join(sorted([team1["name"], team2["name"]]))
            date_str = game_date if game_date else ""
            team1_name = team1["name"].replace(" ", "")
            team2_name = team2["name"].replace(" ", "")

            normalized_entry = {
                "question": question,
                "date": date_str,
                "platform": "kalshi",
                f"{team1_name} BUY": (
                    round(team1_buy, 2) if team1_buy is not None else None
                ),
                f"{team2_name} BUY": (
                    round(team2_buy, 2) if team2_buy is not None else None
                ),
                "kalshi link": (
                    f"{self.kalshi_base_url}"
                    f"{'-'.join(market['market_ticker'].split('-')[:2])}"
                ),
            }

            normalized.append(normalized_entry)

        normalized = self._create_hash_and_save_as_map(normalized)
        return normalized

    def _normalize_polymarket_markets(self) -> dict[str, dict[str, Any]]:
        """Normalize Polymarket market data to standard format."""
        for market in self.polymarket_markets:
            if "question" in market:
                question = market["question"]
                # Clean up CS2 questions: remove "Counter-Strike:" prefix and "(BO1/BO3)" suffix
                if "Counter-Strike:" in question:
                    question = question.split("Counter-Strike:")[-1].strip()
                if "(" in question:
                    question = question.split("(")[0].strip()
                question = question.replace(" vs. ", " vs ")
                market["question"] = question

                # Normalize BUY keys to remove spaces (match Kalshi format)
                buy_keys_to_update = {}
                for key in list(market.keys()):
                    if key.endswith(" BUY") and " " in key:
                        team_name = key.replace(" BUY", "")
                        normalized_team_name = team_name.replace(" ", "")
                        if normalized_team_name != team_name:
                            buy_keys_to_update[key] = f"{normalized_team_name} BUY"

                # Update BUY keys
                for old_key, new_key in buy_keys_to_update.items():
                    if old_key in market:
                        market[new_key] = market.pop(old_key)

            market["platform"] = "polymarket"
            market["polymarket link"] = f"{self.polymarket_base_url}{market['slug']}"

        self.polymarket_markets = self._create_hash_and_save_as_map(
            self.polymarket_markets
        )
        return self.polymarket_markets

    def _create_hash_and_save_as_map(self, data: list[dict]) -> dict:
        """Create hash for each entry and return as dictionary map."""
        for entry in data:
            team1, team2 = sorted(entry["question"].split(" vs "))
            date = entry["date"]
            key = f"{team1}{team2}{date}"
            entry["hash"] = hashlib.sha256(key.encode()).hexdigest()

        new_map = {}

        for entry in data:
            new_map[entry["hash"]] = entry

        return new_map
