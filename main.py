"""Main entry point for the prediction market arbitrage script."""

import argparse
import asyncio
import logging

from sports import cfb, cs2, nba, nfl, nhl

logger = logging.getLogger(__name__)


async def main(quiet: bool = False, enabled_markets: list[str] | None = None):
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

    # Map market names to their corresponding functions
    market_functions = {
        "nba": nba,
        "nfl": nfl,
        "nhl": nhl,
        "cfb": cfb,
        "cs2": cs2,
    }

    # If no markets specified, run all markets
    if enabled_markets is None or len(enabled_markets) == 0:
        enabled_markets = list(market_functions.keys())

    # Get the functions for enabled markets
    tasks = [
        market_functions[market]()
        for market in enabled_markets
        if market in market_functions
    ]

    if not tasks:
        logger.warning(
            "No valid markets specified. Available markets: %s",
            ", ".join(market_functions.keys()),
        )
        return

    logger.info("Running markets: %s", ", ".join(enabled_markets))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prediction market arbitrage script")
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Disable logging output",
    )
    parser.add_argument(
        "--nba",
        action="store_true",
        help="Enable NBA market",
    )
    parser.add_argument(
        "--nfl",
        action="store_true",
        help="Enable NFL market",
    )
    parser.add_argument(
        "--nhl",
        action="store_true",
        help="Enable NHL market",
    )
    parser.add_argument(
        "--cfb",
        action="store_true",
        help="Enable CFB market",
    )
    parser.add_argument(
        "--cs2",
        action="store_true",
        help="Enable CS2 market",
    )
    args = parser.parse_args()

    # Collect enabled markets from arguments
    enabled_markets = []
    if args.nba:
        enabled_markets.append("nba")
    if args.nfl:
        enabled_markets.append("nfl")
    if args.nhl:
        enabled_markets.append("nhl")
    if args.cfb:
        enabled_markets.append("cfb")
    if args.cs2:
        enabled_markets.append("cs2")

    # If no markets specified, pass None to run all markets
    enabled_markets = enabled_markets if enabled_markets else None

    asyncio.run(main(quiet=args.quiet, enabled_markets=enabled_markets))
