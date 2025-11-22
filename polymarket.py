import asyncio
import datetime
import json
import logging
import time

import aiohttp
from dateutil import tz

logger = logging.getLogger(__name__)


class Polymarket:
    GAMMA_MARKET_URL = "https://gamma-api.polymarket.com/markets"
    CLOB_PRICE_URL = "https://clob.polymarket.com/price"

    def __init__(self, tag_id):
        """Initialize Polymarket client with tag ID."""
        self.tag_id = tag_id
        self.market_data = []

    async def get_market_data(self):
        """Fetch and process market data from Polymarket."""
        start_time = time.time()
        logger.info(f"Starting Polymarket market data fetch for tag_id: {self.tag_id}")

        async with aiohttp.ClientSession() as session:
            markets = await self._fetch_games(session)
            if not markets:
                logger.warning("No markets found from Polymarket")
                self.market_data = []
                return []

            logger.info(f"Fetched {len(markets)} markets from Polymarket")

            tasks = []
            questions = []
            for market in markets:
                question = market.get("question", "")
                questions.append(question)
                clob_token_ids = json.loads(market.get("clobTokenIds", "[]"))
                try:
                    team1, team2 = question.replace(" ", "").split("vs.")
                except ValueError:
                    continue

                for i, token in enumerate(clob_token_ids):
                    team = team1 if i == 0 else team2
                    tasks.append(
                        self._fetch_buy_sell_for_token(session, question, team, token)
                    )

            # Limit concurrency to avoid overloading server
            sem = asyncio.Semaphore(8)

            async def sem_task(task):
                async with sem:
                    return await task

            logger.debug(
                f"Fetching prices for {len(tasks)} tokens with concurrency limit of 8"
            )
            results = await asyncio.gather(
                *[sem_task(t) for t in tasks], return_exceptions=True
            )

            question_to_market = {}
            for market in markets:
                question = market.get("question", "")
                if question:
                    question_to_market[question] = {
                        "question": question,
                        "date": self._utc_to_est(market.get("endDate")),
                    }

            failed_count = 0
            for r in results:
                if isinstance(r, Exception):
                    logger.error(f"Request failed: {r}")
                    failed_count += 1
                    continue
                question, team, buy_json, sell_json = r
                market_data = question_to_market.get(question)
                if market_data is not None:
                    market_data[f"{team} BUY"] = (
                        float(buy_json.get("price", 0))
                        if buy_json.get("price")
                        else None
                    )
                    # market_data[f"{team} SELL"] = (
                    #     float(sell_json.get("price", 0))
                    #     if sell_json.get("price")
                    #     else None
                    # )

            elapsed_time = time.time() - start_time
            logger.info(
                f"Polymarket market data fetch completed in {elapsed_time:.2f} seconds. Loaded {len(question_to_market)} markets ({failed_count} requests failed)"
            )
            self.market_data = list(question_to_market.values())
            return self.market_data

    async def _fetch_json(self, session, url, params):
        """Fetch JSON data from URL."""
        start_time = time.time()
        logger.debug(f"Fetching from {url} with params: {params}")
        try:
            async with session.get(url, params=params, timeout=30) as resp:
                resp.raise_for_status()
                data = await resp.json()
                elapsed_time = time.time() - start_time
                logger.debug(f"Fetched from {url} in {elapsed_time:.2f} seconds")
                return data
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                f"Failed to fetch from {url} after {elapsed_time:.2f} seconds: {e}"
            )
            raise

    async def _fetch_games(self, session):
        """Fetch games from Polymarket API."""
        now = datetime.datetime.utcnow()
        one_week = now + datetime.timedelta(days=7)

        query_string = {
            "end_date_min": now.isoformat() + "Z",
            "end_date_max": one_week.isoformat() + "Z",
            "sports_market_types": "moneyline",
            "tag_id": self.tag_id,
        }

        try:
            return await self._fetch_json(session, self.GAMMA_MARKET_URL, query_string)
        except Exception as e:
            logger.error(f"Failed to fetch games: {e}")
            return []

    async def _fetch_buy_sell_for_token(self, session, question, team, token):
        """Fetch buy and sell prices for a token."""
        start_time = time.time()
        buy_task = self._fetch_json(
            session, self.CLOB_PRICE_URL, {"token_id": token, "side": "SELL"}
        )
        sell_task = self._fetch_json(
            session, self.CLOB_PRICE_URL, {"token_id": token, "side": "BUY"}
        )

        buy_json, sell_json = await asyncio.gather(
            buy_task, sell_task, return_exceptions=True
        )

        # Handle exceptions from individual tasks
        if isinstance(buy_json, Exception):
            logger.error(f"Failed to fetch buy price for token {token}: {buy_json}")
            buy_json = {}
        if isinstance(sell_json, Exception):
            logger.error(f"Failed to fetch sell price for token {token}: {sell_json}")
            sell_json = {}

        elapsed_time = time.time() - start_time
        logger.debug(
            f"Fetched prices for token {token} ({team}) in {elapsed_time:.2f} seconds"
        )
        return question, team, buy_json, sell_json

    def _save_to_file(self, path="markets_polymarket.json"):
        """Save market data to JSON file."""
        with open(path, "w") as f:
            json.dump(self.market_data, f, indent=2)
        return path

    def _utc_to_est(self, utc_date_str):
        """Convert UTC datetime string to EST."""
        if not utc_date_str:
            return None

        utc_dt = datetime.datetime.fromisoformat(utc_date_str.replace("Z", "+00:00"))

        eastern = tz.gettz("America/New_York")
        est_dt = utc_dt.astimezone(eastern)

        return est_dt.strftime("%Y-%m-%d")
