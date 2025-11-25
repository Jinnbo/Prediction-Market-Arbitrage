"""Polymarket API client for fetching prediction market data."""

import asyncio
import datetime
import json
import logging
import time
from typing import Any

import aiohttp

from utils import save_to_json, utc_to_est

logger = logging.getLogger(__name__)


class Polymarket:
    """Polymarket Client"""

    GAMMA_MARKET_URL = "https://gamma-api.polymarket.com/markets"
    CLOB_PRICE_URL = "https://clob.polymarket.com/price"

    def __init__(self, tag_id: str, market: str) -> None:
        """Initialize Polymarket client with tag ID."""
        self.tag_id = tag_id
        self.market_data = []
        self.market = market

    async def get_market_data(self) -> list[dict[str, Any]]:
        """Fetch and process market data from Polymarket."""
        start_time = time.time()
        logger.info("Starting Polymarket market data fetch for tag_id: %s", self.tag_id)

        async with aiohttp.ClientSession() as session:
            markets = await self._fetch_games(session)
            if not markets:
                logger.warning("No markets found from Polymarket")
                self.market_data = []
                return []

            logger.info("Fetched %d markets from Polymarket", len(markets))

            tasks = []
            questions = []
            for market in markets:
                question = market.get("question", "")
                questions.append(question)
                clob_token_ids = json.loads(market.get("clobTokenIds", "[]"))
                try:
                    # Handle both "vs." and " vs " formats
                    # First try "vs." format (traditional sports)
                    if " vs " in question:
                        # CS2 format: "Counter-Strike: Team1 vs Team2 (BO1)"
                        # Remove prefix and suffix, then split
                        clean_question = question
                        if "Counter-Strike:" in clean_question:
                            clean_question = clean_question.split("Counter-Strike:")[
                                -1
                            ].strip()
                        if "(" in clean_question:
                            clean_question = clean_question.split("(")[0].strip()
                        team1, team2 = clean_question.split(" vs ", 1)
                        team1 = team1.strip()
                        team2 = team2.strip()
                    else:
                        # Traditional format: "Team1 vs. Team2"
                        team1, team2 = question.replace(" ", "").split("vs.")
                except (ValueError, IndexError):
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
                "Fetching prices for %d tokens with concurrency limit of 8", len(tasks)
            )
            results = await asyncio.gather(
                *[sem_task(t) for t in tasks], return_exceptions=True
            )

            question_to_market = {}
            for market in markets:
                question = market.get("question", "")
                if question:
                    slug = market.get("slug", "")
                    market_entry = {
                        "question": question,
                        "date": utc_to_est(market.get("endDate")),
                    }
                    if slug:
                        market_entry["slug"] = slug
                    question_to_market[question] = market_entry

            failed_count = 0
            for r in results:
                if isinstance(r, Exception):
                    logger.error("Request failed: %s", r)
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

            elapsed_time = time.time() - start_time
            logger.info(
                "Polymarket market data fetch completed in %.2f seconds. Loaded %d markets (%d requests failed)",
                elapsed_time,
                len(question_to_market),
                failed_count,
            )
            self.market_data = list(question_to_market.values())
            save_to_json(
                self.market_data, f"data/{self.market}_markets_polymarket.json"
            )
            return self.market_data

    async def _fetch_json(
        self, session: aiohttp.ClientSession, url: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """Fetch JSON data from URL."""
        start_time = time.time()
        logger.debug("Fetching from %s with params: %s", url, params)
        try:
            async with session.get(url, params=params, timeout=30) as resp:
                resp.raise_for_status()
                data = await resp.json()
                elapsed_time = time.time() - start_time
                logger.debug("Fetched from %s in %.2f seconds", url, elapsed_time)
                return data
        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(
                "Failed to fetch from %s after %.2f seconds: %s", url, elapsed_time, e
            )
            raise

    async def _fetch_games(
        self, session: aiohttp.ClientSession
    ) -> list[dict[str, Any]]:
        """Fetch games from Polymarket API."""
        now = datetime.datetime.utcnow()
        three_weeks = now + datetime.timedelta(days=21)

        query_string = {
            "end_date_min": now.isoformat() + "Z",
            "end_date_max": three_weeks.isoformat() + "Z",
            "sports_market_types": "moneyline",
            "tag_id": self.tag_id,
            "limit": 100,
        }

        try:
            markets = await self._fetch_json(
                session, self.GAMMA_MARKET_URL, query_string
            )
            # Filter to only include open, tradeable markets
            markets = [
                m
                for m in markets
                if not m.get("closed", False) and m.get("acceptingOrders", True)
            ]
            return markets
        except Exception as e:
            logger.error("Failed to fetch games: %s", e)
            return []

    async def _fetch_buy_sell_for_token(
        self, session: aiohttp.ClientSession, question: str, team: str, token: str
    ) -> tuple[str, str, dict[str, Any], dict[str, Any]]:
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
            logger.error("Failed to fetch buy price for token %s: %s", token, buy_json)
            buy_json = {}
        if isinstance(sell_json, Exception):
            logger.error(
                "Failed to fetch sell price for token %s: %s", token, sell_json
            )
            sell_json = {}

        elapsed_time = time.time() - start_time
        logger.debug(
            "Fetched prices for token %s (%s) in %.2f seconds",
            token,
            team,
            elapsed_time,
        )
        return question, team, buy_json, sell_json
