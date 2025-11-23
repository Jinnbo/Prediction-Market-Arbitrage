"""Normalizes NBA market data from different prediction market platforms."""

import hashlib
import json
import os
from collections import defaultdict
from typing import Any


class NormalizeNBAMarkets:
    """Normalizes NBA market data from different prediction market platforms."""

    TEAM_NAME_MAP = {
        # Atlanta
        "ATL": "Hawks",
        "Atlanta": "Hawks",
        # Boston
        "BOS": "Celtics",
        "Boston": "Celtics",
        # Brooklyn
        "BKN": "Nets",
        "Brooklyn": "Nets",
        # Charlotte
        "CHA": "Hornets",
        "Charlotte": "Hornets",
        # Chicago
        "CHI": "Bulls",
        "Chicago": "Bulls",
        # Cleveland
        "CLE": "Cavaliers",
        "Cleveland": "Cavaliers",
        # Dallas
        "DAL": "Mavericks",
        "Dallas": "Mavericks",
        # Denver
        "DEN": "Nuggets",
        "Denver": "Nuggets",
        # Detroit
        "DET": "Pistons",
        "Detroit": "Pistons",
        # Golden State
        "GSW": "Warriors",
        "Golden State": "Warriors",
        # Houston
        "HOU": "Rockets",
        "Houston": "Rockets",
        # Indiana
        "IND": "Pacers",
        "Indiana": "Pacers",
        # Los Angeles teams
        "Los Angeles C": "Clippers",
        "LAC": "Clippers",
        "Los Angeles L": "Lakers",
        "LAL": "Lakers",
        # Memphis
        "MEM": "Grizzlies",
        "Memphis": "Grizzlies",
        # Miami
        "MIA": "Heat",
        "Miami": "Heat",
        # Milwaukee
        "MIL": "Bucks",
        "Milwaukee": "Bucks",
        # Minnesota
        "MIN": "Timberwolves",
        "Minnesota": "Timberwolves",
        # New Orleans
        "NOP": "Pelicans",
        "New Orleans": "Pelicans",
        # New York
        "New York K": "Knicks",
        "NYK": "Knicks",
        # Oklahoma City
        "OKC": "Thunder",
        "Oklahoma City": "Thunder",
        # Orlando
        "ORL": "Magic",
        "Orlando": "Magic",
        # Philadelphia
        "PHI": "76ers",
        "Philadelphia": "76ers",
        # Phoenix
        "PHX": "Suns",
        "Phoenix": "Suns",
        # Portland
        "POR": "Trail Blazers",
        "Portland": "Trail Blazers",
        "TrailBlazers": "Trail Blazers",
        # Sacramento
        "SAC": "Kings",
        "Sacramento": "Kings",
        # San Antonio
        "SAS": "Spurs",
        "San Antonio": "Spurs",
        # Toronto
        "TOR": "Raptors",
        "Toronto": "Raptors",
        # Washington
        "WAS": "Wizards",
        "Washington": "Wizards",
    }

    KALSHI_BASE_NBA_URL = (
        "https://kalshi.com/markets/kxnbagame/professional-basketball-game/"
    )

    def __init__(
        self,
        polymarket_markets: list[dict[str, Any]],
        kalshi_markets: list[dict[str, Any]],
    ) -> None:
        """Initialize normalizer with Polymarket and Kalshi market data."""
        self.polymarket_markets = polymarket_markets
        self.kalshi_markets = kalshi_markets

    def normalize_markets(
        self, output_dir: str = "data", save: bool = True
    ) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
        """Normalize and optionally save market data from both platforms."""
        os.makedirs(output_dir, exist_ok=True)
        normalized_kalshi = self._normalize_kalshi_markets()
        normalized_polymarket = self._normalize_polymarket_markets()

        if save:
            self._save_to_json(
                normalized_kalshi,
                path=os.path.join(output_dir, "nba_markets_kalshi_normalized.json"),
            )
            self._save_to_json(
                normalized_polymarket,
                path=os.path.join(output_dir, "nba_markets_polymarket_normalized.json"),
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

                if team_abbr and team_abbr in self.TEAM_NAME_MAP:
                    team_name = self.TEAM_NAME_MAP[team_abbr]
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
                    f"{self.KALSHI_BASE_NBA_URL}"
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
                market["question"] = market["question"].replace(" vs. ", " vs ")

            market["platform"] = "polymarket"

        self.polymarket_markets = self._create_hash_and_save_as_map(
            self.polymarket_markets
        )
        return self.polymarket_markets

    def _save_to_json(self, data: list[dict], path: str) -> None:
        """Save data to JSON file."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} markets to {path}")

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
