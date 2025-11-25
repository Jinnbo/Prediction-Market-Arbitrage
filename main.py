"""Main entry point for the prediction market arbitrage script."""

import argparse
import asyncio
import logging

from sports import cfb, nba, nfl, nhl

logger = logging.getLogger(__name__)


async def main(quiet: bool = False):
    if not quiet:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.info("Starting prediction market arbitrage script")
    else:
        logging.disable(logging.CRITICAL)

    await asyncio.gather(cfb(), nba(), nfl(), nhl())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prediction market arbitrage script")
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Disable logging output",
    )
    args = parser.parse_args()
    asyncio.run(main(quiet=args.quiet))
