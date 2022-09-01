from typing import List, Dict
from result import Result
from stock_price import StockPrice
from csv_util import ColumnTranslation, read_csv_file


class TradingAlgorithms:
    DEFAULT_MIN_HOLD_MINUTES: int = 30
    DEFAULT_MAX_HOLD_MINUTES: int = 60

    @classmethod
    def ALGORITHMS(cls) -> Dict:
        return {
            1: cls.algorithm_simple,
            2: cls.algorithm_medium,
            3: cls.algorithm_complex,
        }

    @classmethod
    def ALGORITHMS_CHOICES(cls) -> Dict:
        algorithms = cls.ALGORITHMS()
        return {
            algo_num: algo_method.__name__
            for algo_num, algo_method in algorithms.items()
        }

    def __init__(self, csv_filename):
        self.min_hold: int = self.DEFAULT_MIN_HOLD_MINUTES
        self.max_hold: int = self.DEFAULT_MAX_HOLD_MINUTES

        self.init_result: Result = self.read_stock_prices(csv_filename)
        self.stock_prices: List[StockPrice] = self.init_result.result

    def read_stock_prices(self, csv_filename) -> Result:
        column_translations = [
            ColumnTranslation("Time", "minute", int),
            ColumnTranslation("Price", "price", float),
        ]
        result = read_csv_file(csv_filename, column_translations, StockPrice)
        return result

    def run(self, algorithm_choice):
        # todo: find better way to do this
        self.ALGORITHMS()[algorithm_choice](self)

    def algorithm_simple(self):
        print("algorithm_simple")
        print(self.stock_prices)

    def algorithm_complex(self):
        print("algorithm_complex")

    def algorithm_medium(self):
        print("algorithm_medium")
