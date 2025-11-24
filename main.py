"""Main entry point for the prediction market arbitrage script."""

import asyncio
import logging

from sports import nba, nhl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Starting prediction market arbitrage script")

    # await nba()
    await nhl()


if __name__ == "__main__":
    asyncio.run(main())
