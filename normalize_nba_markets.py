import hashlib
import json
import os
from collections import defaultdict


class NormalizeNBAMarkets:

    TEAM_NAME_MAP = {
        # Atlanta
        "ATL": "Hawks",
        "Atlanta": "Hawks",
        "Hawks": "Hawks",
        # Boston
        "BOS": "Celtics",
        "Boston": "Celtics",
        "Celtics": "Celtics",
        # Brooklyn
        "BKN": "Nets",
        "Brooklyn": "Nets",
        "Nets": "Nets",
        # Charlotte
        "CHA": "Hornets",
        "Charlotte": "Hornets",
        "Hornets": "Hornets",
        # Chicago
        "CHI": "Bulls",
        "Chicago": "Bulls",
        "Bulls": "Bulls",
        # Cleveland
        "CLE": "Cavaliers",
        "Cleveland": "Cavaliers",
        "Cavaliers": "Cavaliers",
        # Dallas
        "DAL": "Mavericks",
        "Dallas": "Mavericks",
        "Mavericks": "Mavericks",
        # Denver
        "DEN": "Nuggets",
        "Denver": "Nuggets",
        "Nuggets": "Nuggets",
        # Detroit
        "DET": "Pistons",
        "Detroit": "Pistons",
        "Pistons": "Pistons",
        # Golden State
        "GSW": "Warriors",
        "Golden State": "Warriors",
        "Warriors": "Warriors",
        # Houston
        "HOU": "Rockets",
        "Houston": "Rockets",
        "Rockets": "Rockets",
        # Indiana
        "IND": "Pacers",
        "Indiana": "Pacers",
        "Pacers": "Pacers",
        # Los Angeles teams
        "Los Angeles C": "Clippers",
        "LAC": "Clippers",
        "Clippers": "Clippers",
        "Los Angeles L": "Lakers",
        "LAL": "Lakers",
        "Lakers": "Lakers",
        # Memphis
        "MEM": "Grizzlies",
        "Memphis": "Grizzlies",
        "Grizzlies": "Grizzlies",
        # Miami
        "MIA": "Heat",
        "Miami": "Heat",
        "Heat": "Heat",
        # Milwaukee
        "MIL": "Bucks",
        "Milwaukee": "Bucks",
        "Bucks": "Bucks",
        # Minnesota
        "MIN": "Timberwolves",
        "Minnesota": "Timberwolves",
        "Timberwolves": "Timberwolves",
        # New Orleans
        "NOP": "Pelicans",
        "New Orleans": "Pelicans",
        "Pelicans": "Pelicans",
        # New York
        "New York K": "Knicks",
        "NYK": "Knicks",
        "Knicks": "Knicks",
        # Oklahoma City
        "OKC": "Thunder",
        "Oklahoma City": "Thunder",
        "Thunder": "Thunder",
        # Orlando
        "ORL": "Magic",
        "Orlando": "Magic",
        "Magic": "Magic",
        # Philadelphia
        "PHI": "76ers",
        "Philadelphia": "76ers",
        "76ers": "76ers",
        # Phoenix
        "PHX": "Suns",
        "Phoenix": "Suns",
        "Suns": "Suns",
        # Portland
        "POR": "Trail Blazers",
        "Portland": "Trail Blazers",
        "TrailBlazers": "Trail Blazers",
        "Trail Blazers": "Trail Blazers",
        # Sacramento
        "SAC": "Kings",
        "Sacramento": "Kings",
        "Kings": "Kings",
        # San Antonio
        "SAS": "Spurs",
        "San Antonio": "Spurs",
        "Spurs": "Spurs",
        # Toronto
        "TOR": "Raptors",
        "Toronto": "Raptors",
        "Raptors": "Raptors",
        # Washington
        "WAS": "Wizards",
        "Washington": "Wizards",
        "Wizards": "Wizards",
    }

    def __init__(self, polymarket_markets, kalshi_markets):
        self.polymarket_markets = polymarket_markets
        self.kalshi_markets = kalshi_markets

    def normalize_and_save_markets(self, output_dir="data"):
        os.makedirs(output_dir, exist_ok=True)
        normalized_kalshi = self._normalize_kalshi_markets()
        normalized_polymarket = self._normalize_polymarket_markets()
        self._save_to_json(
            normalized_kalshi,
            path=os.path.join(output_dir, "nba_markets_kalshi_normalized.json"),
        )
        self._save_to_json(
            normalized_polymarket,
            path=os.path.join(output_dir, "nba_markets_polymarket_normalized.json"),
        )

    def _normalize_kalshi_markets(self):
        # Group markets by event_title and game_date
        grouped_markets = defaultdict(list)
        for market in self.kalshi_markets:
            key = (market["event_title"], market["game_date"])
            grouped_markets[key].append(market)

        normalized = []

        for (event_title, game_date), markets in grouped_markets.items():
            # Should have exactly 2 markets (one for each team)
            if len(markets) != 2:
                continue

            # Extract team abbreviations from market_ticker
            # Format: "KXNBAGAME-25NOV15LALMIL-MIL" -> "MIL"
            teams = {}
            for market in markets:
                ticker = market["market_ticker"]
                team_abbr = ticker.split("-")[-1] if "-" in ticker else None

                if team_abbr and team_abbr in self.TEAM_NAME_MAP:
                    team_name = self.TEAM_NAME_MAP[team_abbr]
                    teams[team_abbr] = {"name": team_name, "market": market}

            # Need both teams to create normalized entry
            if len(teams) != 2:
                continue

            # Get team names and markets, sorted alphabetically for consistent ordering
            team_list = sorted(teams.values(), key=lambda x: x["name"])
            team1 = team_list[0]
            team2 = team_list[1]

            # Convert prices from cents (0-100) to decimals (0.0-1.0)
            team1_buy = (
                team1["market"]["yes_bid"] / 100.0
                if team1["market"]["yes_bid"] is not None
                else None
            )
            team1_sell = (
                team1["market"]["yes_ask"] / 100.0
                if team1["market"]["yes_ask"] is not None
                else None
            )
            team2_buy = (
                team2["market"]["yes_bid"] / 100.0
                if team2["market"]["yes_bid"] is not None
                else None
            )
            team2_sell = (
                team2["market"]["yes_ask"] / 100.0
                if team2["market"]["yes_ask"] is not None
                else None
            )

            question = " vs ".join(sorted([team1["name"], team2["name"]]))
            date_str = game_date if game_date else ""

            normalized_entry = {
                "question": question,
                "date": date_str,
                f"{team1['name']} BUY": (
                    round(team1_buy, 2) if team1_buy is not None else None
                ),
                f"{team1['name']} SELL": (
                    round(team1_sell, 2) if team1_sell is not None else None
                ),
                f"{team2['name']} BUY": (
                    round(team2_buy, 2) if team2_buy is not None else None
                ),
                f"{team2['name']} SELL": (
                    round(team2_sell, 2) if team2_sell is not None else None
                ),
            }

            normalized.append(normalized_entry)
            self._create_hashes(normalized)

        return normalized

    def _normalize_polymarket_markets(self):
        for market in self.polymarket_markets:
            if "question" in market:
                market["question"] = market["question"].replace(" vs. ", " vs ")
        self._create_hashes(self.polymarket_markets)
        return self.polymarket_markets

    def _save_to_json(self, data: list[dict], path: str) -> None:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} markets to {path}")

    def _create_hashes(self, data: list[dict]) -> None:
        for entry in data:
            team1, team2 = sorted(entry["question"].split(" vs "))
            date = entry["date"]
            key = f"{team1}{team2}{date}"
            entry["hash"] = hashlib.sha256(key.encode()).hexdigest()
