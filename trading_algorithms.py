from typing import List, Dict
import pprint
import logging

from result import Result
from market_condition import MarketCondition
from stock_prices import StockPrices
from csv_util import ColumnTranslation, read_csv_file
from trade_point import TradePoint


class TradingAlgorithms:
    DEFAULT_MIN_HOLD_MINUTES: int = 30
    DEFAULT_MAX_HOLD_MINUTES: int = 60

    @classmethod
    def ALGORITHMS(cls) -> Dict:
        return {
            1: cls.algorithm_least_purchases,
            2: cls.algorithm_most_purchases,
            3: cls.algorithm_new_unimplemented,
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
        self.init_result: Result = self.read_market_conditions(csv_filename)
        # TODO: It would be better if TradingAlgorithms constructor raised exception if read_stock_prices failed!
        # TODO: If the number of stock_prices < min_hold, then flag the error
        self.stock_prices = StockPrices(market_conditions=self.init_result.result)

    def read_market_conditions(self, csv_filename) -> Result:
        column_translations = [
            ColumnTranslation("Time", "minute", int),
            ColumnTranslation("Price", "price", float),
        ]
        result = read_csv_file(
            csv_filename, column_translations, row_object_type=MarketCondition
        )
        return result

    def run(self, algorithm_choice) -> List[TradePoint]:
        # TODO: find better way to do this
        return self.ALGORITHMS()[algorithm_choice](self)

    def algorithm_least_purchases(self) -> List[TradePoint]:
        logging.info("Running: Algorithm of least purchases")
        curr_offset = 0
        market_conditions = self.stock_prices.market_conditions
        trade_points: List[TradePoint] = []
        while curr_offset + self.min_hold < len(market_conditions):
            purchase_range_min = curr_offset + self.min_hold
            purchase_range_max = min(
                curr_offset + self.max_hold + 1, len(market_conditions)
            )
            max_price_in_purchase_range = 0
            best_market_condition: MarketCondition
            for i in range(purchase_range_min, purchase_range_max):
                if market_conditions[i].price > max_price_in_purchase_range:
                    max_price_in_purchase_range = market_conditions[i].price
                    best_market_condition = market_conditions[i]
            if max_price_in_purchase_range > market_conditions[curr_offset].price:
                trade_point = TradePoint(market_conditions[curr_offset])
                trade_point.sell_point_determined(best_market_condition)
                trade_points.append(trade_point)
                curr_offset = i + 1
            else:
                curr_offset += 1

        logging.debug(f"{pprint.pformat(trade_points)=}")
        return trade_points

    def algorithm_most_purchases(self) -> List[TradePoint]:
        # TODO: This algorithm is incomplete (does not honor the max hold limit).
        #       The current implement is too complex to read and understand.
        #       Can be re-implemented.
        logging.info("Running: Algorithm of most purchases")
        trade_points: List[TradePoint] = []
        prev_offset = 0
        step = self.min_hold
        market_condition_prev = self.stock_prices.market_conditions[prev_offset]
        market_condition_curr = self.stock_prices.market_conditions[
            prev_offset + step
        ]  # TODO: boundary check
        potent_purchase_point = None
        purchase_point = None
        sell_point = None
        while market_condition_curr:
            if market_condition_curr.price > market_condition_prev.price:
                prev_offset = prev_offset + step
                step = 1
                if not potent_purchase_point:
                    potent_purchase_point = market_condition_prev
            else:
                if potent_purchase_point and (
                    potent_purchase_point is not market_condition_prev
                ):
                    purchase_point = potent_purchase_point
                    sell_point = market_condition_prev
                    trade_point = TradePoint(purchase_point)
                    trade_point.sell_point_determined(sell_point)
                    trade_points.append(trade_point)
                    potent_purchase_point = None
                    step = self.min_hold
                prev_offset += 1

            market_condition_prev = (
                self.stock_prices.market_conditions[prev_offset]
                if prev_offset < len(self.stock_prices.market_conditions)
                else None
            )
            market_condition_curr = (
                self.stock_prices.market_conditions[prev_offset + step]
                if (prev_offset + step) < len(self.stock_prices.market_conditions)
                else None
            )
            # logging.debug(f"{market_condition_prev=} {market_condition_curr=}")

        logging.debug(f"{pprint.pformat(trade_points)=}")
        return trade_points

    def algorithm_new_unimplemented(self) -> List[TradePoint]:
        logging.info("algorithm_new_unimplemented")
        print("This algorithm is not yet implemented")
        trade_points: List[TradePoint] = []
        return trade_points
