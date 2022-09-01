from typing import Dict
from result import Result
from trade_point import TradePoint
from csv_util import ColumnTranslation, read_csv_file


class TradingAlgorithms:
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
        self.init_result = self.prepare_trading_points(csv_filename)
        self.trading_points = self.init_result.result

    def prepare_trading_points(self, csv_filename) -> Result:
        column_translations = [
            ColumnTranslation("Time", "minute", int),
            ColumnTranslation("Price", "price", float),
        ]
        result = read_csv_file(csv_filename, column_translations, TradePoint)
        return result

    def run(self, algorithm_choice):
        # todo: find better way than this
        self.ALGORITHMS()[algorithm_choice](self)

    def algorithm_simple(self):
        print("algorithm_simple")
        print(self.trading_points)

    def algorithm_complex(self):
        print("algorithm_complex")

    def algorithm_medium(self):
        print("algorithm_medium")
