"""Main entry point for the prediction market arbitrage script."""

import argparse
import asyncio
import logging

from sports import cfb, cs2, nba, nfl, nhl

logger = logging.getLogger(__name__)


async def main(quiet: bool = False):
    """Main entry point for the prediction market arbitrage script."""
    if not quiet:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.info("Starting prediction market arbitrage script")
    else:
        logging.disable(logging.CRITICAL)

    # await asyncio.gather(cfb(), cs2(), nba(), nfl(), nhl())
    await asyncio.gather(nba(), nfl())


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
