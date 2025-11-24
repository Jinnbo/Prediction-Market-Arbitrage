"""Arbitrage calculator for prediction market opportunities."""

import logging
import os
from typing import Any

from supabase import write_nba_to_supabase
from utils import save_to_json

logger = logging.getLogger(__name__)


class ArbitrageNBACalculator:
    def __init__(
        self, market_1: dict[str, dict[str, Any]], market_2: dict[str, dict[str, Any]]
    ) -> None:
        """Initialize calculator with Polymarket and Kalshi market data."""
        self.market_1 = market_1
        self.market_2 = market_2
        self.opportunities: list[dict[str, Any]] = []

    def calculate(self) -> None:
        """Calculate and print arbitrage opportunities."""
        # Find all market hashes that exist in both platforms
        common_hashes = set(self.market_1.keys()) & set(self.market_2.keys())
        logger.info("Found %d markets present on both platforms", len(common_hashes))

        opportunities = []

        for market_hash in common_hashes:
            market_1_data = self.market_1[market_hash]
            market_2_data = self.market_2[market_hash]

            # Extract team names and prices from both markets by finding all " BUY" keys
            # This handles cases where question order differs between platforms
            team_prices_m1 = {}
            team_prices_m2 = {}

            for key, value in market_1_data.items():
                if key.endswith(" BUY") and value is not None:
                    team_name = key.replace(" BUY", "")
                    team_prices_m1[team_name] = value

            for key, value in market_2_data.items():
                if key.endswith(" BUY") and value is not None:
                    team_name = key.replace(" BUY", "")
                    team_prices_m2[team_name] = value

            # Get the set of teams present in both markets
            common_teams = set(team_prices_m1.keys()) & set(team_prices_m2.keys())
            if len(common_teams) != 2:
                continue

            # Convert to sorted list for consistent ordering
            teams = sorted(list(common_teams))
            team1_name = teams[0]
            team2_name = teams[1]

            # Get prices for both teams from both markets
            team1_price_m1 = team_prices_m1[team1_name]
            team2_price_m1 = team_prices_m1[team2_name]
            team1_price_m2 = team_prices_m2[team1_name]
            team2_price_m2 = team_prices_m2[team2_name]

            # Get question for output (use the one that exists)
            question = market_1_data.get("question") or market_2_data.get("question")
            if not question:
                continue

            # Determine which platform is which
            platform_1 = market_1_data.get("platform", "polymarket")
            platform_2 = market_2_data.get("platform", "kalshi")

            # Try both arbitrage strategies and pick the best one that uses different platforms
            # Strategy 1: Buy Team1 on platform with lower Team1 price, Team2 on platform with lower Team2 price
            if team1_price_m1 < team1_price_m2:
                team1_platform_1 = platform_1
                team1_price_1 = team1_price_m1
            else:
                team1_platform_1 = platform_2
                team1_price_1 = team1_price_m2

            if team2_price_m1 < team2_price_m2:
                team2_platform_1 = platform_1
                team2_price_1 = team2_price_m1
            else:
                team2_platform_1 = platform_2
                team2_price_1 = team2_price_m2

            total_cost_1 = team1_price_1 + team2_price_1
            profit_1 = 1.0 - total_cost_1
            uses_different_platforms_1 = team1_platform_1 != team2_platform_1

            # Strategy 2: Buy Team1 on platform with higher Team1 price, Team2 on platform with lower Team2 price
            if team1_price_m1 > team1_price_m2:
                team1_platform_2 = platform_1
                team1_price_2 = team1_price_m1
            else:
                team1_platform_2 = platform_2
                team1_price_2 = team1_price_m2

            if team2_price_m1 < team2_price_m2:
                team2_platform_2 = platform_1
                team2_price_2 = team2_price_m1
            else:
                team2_platform_2 = platform_2
                team2_price_2 = team2_price_m2

            total_cost_2 = team1_price_2 + team2_price_2
            profit_2 = 1.0 - total_cost_2
            uses_different_platforms_2 = team1_platform_2 != team2_platform_2

            # Strategy 3: Buy Team1 on platform with lower Team1 price, Team2 on platform with higher Team2 price
            if team1_price_m1 < team1_price_m2:
                team1_platform_3 = platform_1
                team1_price_3 = team1_price_m1
            else:
                team1_platform_3 = platform_2
                team1_price_3 = team1_price_m2

            if team2_price_m1 > team2_price_m2:
                team2_platform_3 = platform_1
                team2_price_3 = team2_price_m1
            else:
                team2_platform_3 = platform_2
                team2_price_3 = team2_price_m2

            total_cost_3 = team1_price_3 + team2_price_3
            profit_3 = 1.0 - total_cost_3
            uses_different_platforms_3 = team1_platform_3 != team2_platform_3

            # Strategy 4: Buy Team1 on platform with higher Team1 price, Team2 on platform with higher Team2 price
            if team1_price_m1 > team1_price_m2:
                team1_platform_4 = platform_1
                team1_price_4 = team1_price_m1
            else:
                team1_platform_4 = platform_2
                team1_price_4 = team1_price_m2

            if team2_price_m1 > team2_price_m2:
                team2_platform_4 = platform_1
                team2_price_4 = team2_price_m1
            else:
                team2_platform_4 = platform_2
                team2_price_4 = team2_price_m2

            total_cost_4 = team1_price_4 + team2_price_4
            profit_4 = 1.0 - total_cost_4
            uses_different_platforms_4 = team1_platform_4 != team2_platform_4

            # Pick the best strategy that uses different platforms
            strategies = [
                (
                    profit_1,
                    team1_platform_1,
                    team1_price_1,
                    team2_platform_1,
                    team2_price_1,
                    uses_different_platforms_1,
                ),
                (
                    profit_2,
                    team1_platform_2,
                    team1_price_2,
                    team2_platform_2,
                    team2_price_2,
                    uses_different_platforms_2,
                ),
                (
                    profit_3,
                    team1_platform_3,
                    team1_price_3,
                    team2_platform_3,
                    team2_price_3,
                    uses_different_platforms_3,
                ),
                (
                    profit_4,
                    team1_platform_4,
                    team1_price_4,
                    team2_platform_4,
                    team2_price_4,
                    uses_different_platforms_4,
                ),
            ]

            # Filter to only strategies that use different platforms, then pick the best profit
            valid_strategies = [
                s for s in strategies if s[5]
            ]  # s[5] is uses_different_platforms
            if not valid_strategies:
                continue  # Skip if no strategy uses different platforms

            # Pick the strategy with the best profit (highest, even if negative for debugging)
            best_strategy = max(valid_strategies, key=lambda x: x[0])
            profit, team1_platform, team1_price, team2_platform, team2_price, _ = (
                best_strategy
            )

            # Only include opportunities where we buy from different platforms
            # (true arbitrage requires buying from different platforms)
            if profit:
                # Get kalshi link from whichever market has it
                kalshi_link = None
                if "kalshi link" in market_1_data:
                    kalshi_link = market_1_data["kalshi link"]
                elif "kalshi link" in market_2_data:
                    kalshi_link = market_2_data["kalshi link"]

                polymarket_link = None
                if "polymarket link" in market_1_data:
                    polymarket_link = market_1_data["polymarket link"]
                elif "polymarket link" in market_2_data:
                    polymarket_link = market_2_data["polymarket link"]

                opportunity = {
                    "question": question,
                    "date": market_1_data.get("date") or market_2_data.get("date"),
                    "kalshi": f"{team1_name}|{team1_price}",
                    "polymarket": f"{team2_name}|{team2_price}",
                    "profit": round(profit, 4),
                    "kalshi_link": kalshi_link,
                    "polymarket_link": polymarket_link,
                }
                write_nba_to_supabase(opportunity)
                opportunities.append(opportunity)

        # Sort by profit (descending) - most profitable first
        opportunities.sort(key=lambda x: x["profit"], reverse=True)

        self.opportunities = opportunities
        logger.info("Found %d profitable arbitrage opportunities", len(opportunities))

        # Save results
        self._save_to_json()

    def _save_to_json(self) -> None:
        """Save results to JSON file."""
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "arbitrage_opportunities.json")
        save_to_json(self.opportunities, output_path)
        logger.info("Saved arbitrage opportunities to %s", output_path)
