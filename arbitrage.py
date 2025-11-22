class ArbitrageCalculator:
    def __init__(self, market_1: dict[dict], market_2: dict[dict]):
        """Initialize calculator with Polymarket and Kalshi market data."""
        self.market_1 = market_1
        self.market_2 = market_2

    def calculate(self):
        """Calculate and print arbitrage opportunities."""
        market_2 = self.market_2
        for hash_1, market_1_item in self.market_1.items():
            team_1, team_2 = market_1_item["question"].replace(" ", "").split("vs")
            market_2_item = market_2.get(hash_1, "")
            if hash_1 in market_2 and len(market_1_item) == len(market_2_item):

                market_1_team_1_buy = market_1_item[f"{team_1} BUY"]
                market_1_team_2_buy = market_1_item[f"{team_2} BUY"]

                market_2_team_1_buy = market_2_item[f"{team_1} BUY"]
                market_2_team_2_buy = market_2_item[f"{team_2} BUY"]

                team_1_min_buy = min(market_1_team_1_buy, market_2_team_1_buy)
                team_2_min_buy = min(market_1_team_2_buy, market_2_team_2_buy)

                if team_1_min_buy + team_2_min_buy < 1:
                    print("Arbitrage Opportunity Found")
                    print(
                        f"  Buy {team_1} @ {team_1_min_buy} in Polymarket\n  Buy {team_2} @ {team_2_min_buy} in Kalshi"
                    )

    def _save_to_json(self):
        """Save results to JSON file."""
        pass
