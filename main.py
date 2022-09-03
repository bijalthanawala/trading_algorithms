import sys
import argparse
import logging
import pprint
from typing import List

from src.result import Result
from src.csv_util import ColumnTranslation, read_csv_file
from src.market_condition import MarketCondition
from src.trade_point import TradePoint
from src.trading_algorithms import TradingAlgorithms

DEFAULT_CSV_FILENAME = "test/market_conditions_100.csv"


def parse_arguments(unparsed_args: List[str]) -> argparse.Namespace:
    algorithm_choices = TradingAlgorithms.ALGORITHMS_CHOICES()
    parser = argparse.ArgumentParser(
        description="Trading Algorithm", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--file",
        "-f",
        default=DEFAULT_CSV_FILENAME,
        help=f"Name of the input CSV file (Default={DEFAULT_CSV_FILENAME})",
    )
    parser.add_argument(
        "--algorithm",
        "-a",
        type=int,
        default=1,
        choices=algorithm_choices.keys(),
        help=f"Specify one of the algorithm numbers (Default=1)\n{pprint.pformat(algorithm_choices)}",
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parsed_args = parser.parse_args(unparsed_args)
    return parsed_args


def setup_logger(verbosity: int) -> None:
    level_to_set = logging.WARNING
    if verbosity >= 2:
        level_to_set = logging.DEBUG
    elif verbosity == 1:
        level_to_set = logging.INFO
    logging.basicConfig(format="%(message)s", level=level_to_set)


def read_market_conditions(csv_filename) -> Result:
    column_translations = [
        ColumnTranslation("Time", "minute", int),
        ColumnTranslation("Price", "price", float),
    ]
    result = read_csv_file(
        csv_filename, column_translations, row_object_type=MarketCondition
    )
    # TODO: If the number of market_conditions < min_hold, then flag the error
    return result


def main(sys_argv: List[str]) -> bool:
    parsed_args = parse_arguments(sys_argv[1:])
    setup_logger(parsed_args.verbose)

    result = read_market_conditions(csv_filename=parsed_args.file)
    if not result.isSuccess:
        print(f"Error encountered: {result.message}")
        print("Please fix the above error and rerun")
        return result.isSuccess

    market_conditions: List[MarketCondition] = result.result
    trading_algorithms = TradingAlgorithms(market_conditions)

    trading_points: List[TradePoint] = trading_algorithms.run(parsed_args.algorithm)
    total_profit: float = 0.0
    print("Trades are:")
    for tp in trading_points:
        total_profit += tp.profit
        print(tp)
    print(f"Total profit {total_profit:.4f}")

    return True


if __name__ == "__main__":
    main(sys.argv)
