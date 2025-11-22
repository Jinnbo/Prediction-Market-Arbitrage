import asyncio
import datetime
import json
import logging
import time

import aiohttp
from dateutil import tz


class Polymarket:
    GAMMA_MARKET_URL = "https://gamma-api.polymarket.com/markets"
    CLOB_PRICE_URL = "https://clob.polymarket.com/price"

    def __init__(self, tag_id):
        """Initialize Polymarket client with tag ID."""

        self.tag_id = tag_id
        self.market_data = []
        self.logger = logging.getLogger(self.__class__.__name__)

    async def get_market_data(self):
        """Fetch and process market data from Polymarket."""

        async with aiohttp.ClientSession() as session:
            markets = await self._fetch_games(session)
            if not markets:
                self.market_data = []
                return []

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
            concurrency_limit = max(1, min(24, len(tasks)))
            sem = asyncio.Semaphore(concurrency_limit)

            async def sem_task(task):
                async with sem:
                    return await task

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
            for r in results:
                if isinstance(r, Exception):
                    print(f"Request failed: {r}")
                    continue
                question, team, buy_json, sell_json = r
                market_data = question_to_market.get(question)
                if market_data is not None:
                    market_data[f"{team} BUY"] = (
                        float(buy_json.get("price", 0))
                        if buy_json.get("price")
                        else None
                    )
                    market_data[f"{team} SELL"] = (
                        float(sell_json.get("price", 0))
                        if sell_json.get("price")
                        else None
                    )

            self.market_data = list(question_to_market.values())
            return self.market_data

    async def _fetch_json(self, session, url, params):
        """Fetch JSON data from URL."""

        start = time.perf_counter()
        try:
            async with session.get(url, params=params, timeout=30) as resp:
                data = await resp.json()
            duration = time.perf_counter() - start
            self.logger.info(
                "Polymarket fetch %s in %.2fs params=%s", url, duration, params
            )
            return data
        except Exception as exc:
            duration = time.perf_counter() - start
            self.logger.warning(
                "Polymarket fetch failed in %.2fs url=%s params=%s error=%s",
                duration,
                url,
                params,
                exc,
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
            print(f"Failed to fetch games: {e}")
            return []

    async def _fetch_buy_sell_for_token(self, session, question, team, token):
        """Fetch buy and sell prices for a token."""

        buy_task = self._fetch_json(
            session, self.CLOB_PRICE_URL, {"token_id": token, "side": "SELL"}
        )
        sell_task = self._fetch_json(
            session, self.CLOB_PRICE_URL, {"token_id": token, "side": "BUY"}
        )

        buy_json, sell_json = await asyncio.gather(buy_task, sell_task)
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
