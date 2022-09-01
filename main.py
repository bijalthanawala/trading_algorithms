from dataclasses import dataclass
import sys
import csv
import argparse
import logging
import pprint
from typing import List, Any

DEFAULT_CSV_FILENAME = "data_10.csv"
ALGORITHMS_LIST = {
    1: "Algorithm x",
    2: "Algorithm y",
    3: "Algorithm z",
}

# todo: Move this class to a different file later
@dataclass
class TradePoint:
    minute: int
    price: str


# todo: Move this class to a different file later
@dataclass
class Result:
    isSuccess: bool
    message: str
    result: Any


# todo: Move this class to a different file later
class column_translation:
    def __init__(self, column_name, column_name_xlat, column_type):
        self.column_name = column_name
        self.column_name_xlat = column_name_xlat
        self.column_type = column_type


# todo: Start this method here initially. Split, refactor and move to a different file/module later
def read_csv_file(csv_filename: str) -> Result:
    trade_points: List[TradePoint] = []
    column_minute = column_translation("Time", "minute", int)
    column_price = column_translation("Price", "price", float)

    column_translations = []
    column_translations.append(column_minute)
    column_translations.append(column_price)

    try:
        with open(
            csv_filename, newline="", encoding="ascii", errors="ignore"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tp = TradePoint(
                    **{
                        translation.column_name_xlat: translation.column_type(
                            row[translation.column_name]
                        )
                        for translation in column_translations
                    }
                )
                print(tp)
                trade_points.append(tp)
    except Exception as ex:
        return Result(isSuccess=False, message=str(ex), result=None)

    print(trade_points)

    return Result(isSuccess=True, message="", result=trade_points)


def parse_arguments(unparsed_args: List[str]) -> argparse.Namespace:
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
        choices=ALGORITHMS_LIST.keys(),
        help=f"Specify one of the algorithm numbers (Default=1)\n{pprint.pformat(ALGORITHMS_LIST)}",
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    parsed_args = parser.parse_args(unparsed_args)
    return parsed_args


def setup_logger(parsed_args: argparse.Namespace) -> None:
    level_to_set = logging.WARNING
    if parsed_args.verbose >= 2:
        level_to_set = logging.DEBUG
    elif parsed_args.verbose == 1:
        level_to_set = logging.INFO
    logging.basicConfig(format="%(message)s", level=level_to_set)


def main(sys_argv: List[str]) -> bool:
    parsed_args = parse_arguments(sys_argv[1:])
    setup_logger(parsed_args)
    result = read_csv_file(parsed_args.file)

    if not result.isSuccess:
        print(f"Error encountered: {result.message}")
        print("Please fix the above error and rerun")
        return result.isSuccess

    trade_points = result.result
    print(trade_points)

    return True


if __name__ == "__main__":
    main(sys.argv)
