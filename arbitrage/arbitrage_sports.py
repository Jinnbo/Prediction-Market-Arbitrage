"""Arbitrage calculator for prediction market opportunities."""

import logging
import os
from typing import Any

from supabase_client import write_sports_arbitrage_to_supabase
from utils import save_to_json

logger = logging.getLogger(__name__)


class ArbitrageSportsCalculator:
    """Arbitrage calculator for sports markets."""

    def __init__(
        self,
        kalshi_markets: dict[str, dict[str, Any]],
        polymarket_markets: dict[str, dict[str, Any]],
        sport: str,
    ) -> None:
        """Initialize calculator with Polymarket and Kalshi market data."""
        self.kalshi_markets = kalshi_markets
        self.polymarket_markets = polymarket_markets
        self.opportunities: list[dict[str, Any]] = []
        self.sport = sport

    def calculate(self) -> None:
        """Calculate and print arbitrage opportunities."""
        # Find all market hashes that exist in both platforms
        common_hashes = set(self.kalshi_markets.keys()) & set(
            self.polymarket_markets.keys()
        )
        logger.info("Found %d markets present on both platforms", len(common_hashes))

        opportunities = []

        for market_hash in common_hashes:
            kalshi_data = self.kalshi_markets[market_hash]
            polymarket_data = self.polymarket_markets[market_hash]

            # Extract team names and prices from both markets by finding all " BUY" keys
            # This handles cases where question order differs between platforms
            kalshi_team_prices = {}
            polymarket_team_prices = {}

            for key, value in kalshi_data.items():
                if key.endswith(" BUY") and value is not None:
                    team_name = key.replace(" BUY", "")
                    kalshi_team_prices[team_name] = value

            for key, value in polymarket_data.items():
                if key.endswith(" BUY") and value is not None:
                    team_name = key.replace(" BUY", "")
                    polymarket_team_prices[team_name] = value

            # Get the set of teams present in both markets
            common_teams = set(kalshi_team_prices.keys()) & set(
                polymarket_team_prices.keys()
            )
            if len(common_teams) != 2:
                continue

            # Convert to sorted list for consistent ordering
            teams = sorted(list(common_teams))
            team1_name = teams[0]
            team2_name = teams[1]

            # Get prices for both teams from both markets
            team1_price_kalshi = kalshi_team_prices[team1_name]
            team2_price_kalshi = kalshi_team_prices[team2_name]
            team1_price_polymarket = polymarket_team_prices[team1_name]
            team2_price_polymarket = polymarket_team_prices[team2_name]

            # Get question for output (use the one that exists)
            question = kalshi_data.get("question") or polymarket_data.get("question")
            if not question:
                continue

            # Determine which platform is which
            platform_kalshi = kalshi_data.get("platform", "kalshi")
            platform_polymarket = polymarket_data.get("platform", "polymarket")

            # Try both arbitrage strategies and pick the best one that uses different platforms
            # Strategy 1: Buy Team1 on platform with lower Team1 price, Team2 on platform with lower Team2 price
            if team1_price_kalshi < team1_price_polymarket:
                team1_platform_1 = platform_kalshi
                team1_price_1 = team1_price_kalshi
            else:
                team1_platform_1 = platform_polymarket
                team1_price_1 = team1_price_polymarket

            if team2_price_kalshi < team2_price_polymarket:
                team2_platform_1 = platform_kalshi
                team2_price_1 = team2_price_kalshi
            else:
                team2_platform_1 = platform_polymarket
                team2_price_1 = team2_price_polymarket

            total_cost_1 = team1_price_1 + team2_price_1
            profit_1 = 1.0 - total_cost_1
            uses_different_platforms_1 = team1_platform_1 != team2_platform_1

            # Strategy 2: Buy Team1 on platform with higher Team1 price, Team2 on platform with lower Team2 price
            if team1_price_kalshi > team1_price_polymarket:
                team1_platform_2 = platform_kalshi
                team1_price_2 = team1_price_kalshi
            else:
                team1_platform_2 = platform_polymarket
                team1_price_2 = team1_price_polymarket

            if team2_price_kalshi < team2_price_polymarket:
                team2_platform_2 = platform_kalshi
                team2_price_2 = team2_price_kalshi
            else:
                team2_platform_2 = platform_polymarket
                team2_price_2 = team2_price_polymarket

            total_cost_2 = team1_price_2 + team2_price_2
            profit_2 = 1.0 - total_cost_2
            uses_different_platforms_2 = team1_platform_2 != team2_platform_2

            # Strategy 3: Buy Team1 on platform with lower Team1 price, Team2 on platform with higher Team2 price
            if team1_price_kalshi < team1_price_polymarket:
                team1_platform_3 = platform_kalshi
                team1_price_3 = team1_price_kalshi
            else:
                team1_platform_3 = platform_polymarket
                team1_price_3 = team1_price_polymarket

            if team2_price_kalshi > team2_price_polymarket:
                team2_platform_3 = platform_kalshi
                team2_price_3 = team2_price_kalshi
            else:
                team2_platform_3 = platform_polymarket
                team2_price_3 = team2_price_polymarket

            total_cost_3 = team1_price_3 + team2_price_3
            profit_3 = 1.0 - total_cost_3
            uses_different_platforms_3 = team1_platform_3 != team2_platform_3

            # Strategy 4: Buy Team1 on platform with higher Team1 price, Team2 on platform with higher Team2 price
            if team1_price_kalshi > team1_price_polymarket:
                team1_platform_4 = platform_kalshi
                team1_price_4 = team1_price_kalshi
            else:
                team1_platform_4 = platform_polymarket
                team1_price_4 = team1_price_polymarket

            if team2_price_kalshi > team2_price_polymarket:
                team2_platform_4 = platform_kalshi
                team2_price_4 = team2_price_kalshi
            else:
                team2_platform_4 = platform_polymarket
                team2_price_4 = team2_price_polymarket

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

            if profit:  # TODO: Add profit threshold
                kalshi_link = None
                if "kalshi link" in kalshi_data:
                    kalshi_link = kalshi_data["kalshi link"]
                elif "kalshi link" in polymarket_data:
                    kalshi_link = polymarket_data["kalshi link"]

                polymarket_link = None
                if "polymarket link" in kalshi_data:
                    polymarket_link = kalshi_data["polymarket link"]
                elif "polymarket link" in polymarket_data:
                    polymarket_link = polymarket_data["polymarket link"]

                opportunity = {
                    "question": question,
                    "date": kalshi_data.get("date") or polymarket_data.get("date"),
                    "kalshi": f"{team1_name}|{team1_price}",
                    "polymarket": f"{team2_name}|{team2_price}",
                    "profit": round(profit, 4),
                    "kalshi_link": kalshi_link,
                    "polymarket_link": polymarket_link,
                    "sport": self.sport,
                }
                opportunities.append(opportunity)

        # Sort by profit (descending) - most profitable first
        opportunities.sort(key=lambda x: x["profit"], reverse=True)

        self.opportunities = opportunities
        logger.info("Found %d profitable arbitrage opportunities", len(opportunities))

        # Write to Supabase
        write_sports_arbitrage_to_supabase(opportunities)

        # Save results
        self._save_to_json()

    def _save_to_json(self) -> None:
        """Save results to JSON file."""
        output_dir = "data"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(
            output_dir, f"arbitrage_opportunities_{self.sport}.json"
        )
        save_to_json(self.opportunities, output_path)
        logger.info("Saved arbitrage opportunities to %s", output_path)
