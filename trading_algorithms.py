from typing import List, Dict, Tuple, Any
import pprint
import logging

from result import Result
from market_condition import MarketCondition
from csv_util import ColumnTranslation, read_csv_file
from trade_point import TradePoint


class TradingAlgorithms:
    DEFAULT_MIN_HOLD_MINUTES: int = 30
    DEFAULT_MAX_HOLD_MINUTES: int = 60

    @classmethod
    def ALGORITHMS(cls) -> Dict:
        return {
            1: cls.algorithm_least_purchases,
            2: cls.algorithm_quick_purchases,
            3: cls.algorithm_most_purchases,
            4: cls.algorithm_new_unimplemented,
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
        # TODO: It would be better if TradingAlgorithms constructor raised exception if read_market_conditions failed!
        # TODO: If the number of market_conditions < min_hold, then flag the error
        self.market_conditions: List[MarketCondition] = self.init_result.result

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
        # TODO: Find better way to do this, so that we do not have call this method with 'self' explicitly
        return self.ALGORITHMS()[algorithm_choice](self)

    # Allow only kwargs and avoid possible errors
    def get_purchase_range(
        self, *, curr_offset: int, num_market_conditions: int
    ) -> Tuple[int, int]:
        purchase_range_min = curr_offset + self.min_hold
        purchase_range_max = min(curr_offset + self.max_hold + 1, num_market_conditions)
        return (purchase_range_min, purchase_range_max)

    def algorithm_least_purchases(self) -> List[TradePoint]:
        """
        Steps for the Least Purchase algorithm.
        Step A) Starting with the very first minute M
        Step B) Determine the allowed sell time-window for that minute
        Step C) In that range find the maximum price
        Step D) If the found maximum price (say at minute N), is greater then the price at minute M then
                perform the trade i.e. buy at M and sell at N
        Step E) If the trade was performed, skip to the minute N+1 and goto Step B
        Step F) If the trade was not performed, continue with minute M+1, and goto Step B

        PRO:
        - Easy to understand
        - Easy to implement

        CONS:
        - This algorithm is very inefficient at profit-making because it does not buy-sell often.
        - This algorithm culd also be very slow-performing in the following case:
            If the prices are constantly or mostly declining then Step C would end up finding maximum price
            in consecutive overlapping time-ranges
        """
        logging.info("Running: Algorithm of least purchases")
        trade_points: List[TradePoint] = []

        # Step A
        curr_offset = 0
        while curr_offset + self.min_hold < len(self.market_conditions):

            # Step B
            purchase_range_min, purchase_range_max = self.get_purchase_range(
                curr_offset=curr_offset,
                num_market_conditions=len(self.market_conditions),
            )

            # Step C
            max_price_in_purchase_range: float = 0.0
            max_price_offset: int = 0
            best_market_condition: MarketCondition
            # TODO: This part of finding maximum can use some improvements
            #       by using some knowledge from previous iteration
            #       However, the profit-making ability of this particular algorithm
            #       is so low that this improvement is not justified
            for i in range(purchase_range_min, purchase_range_max):
                if self.market_conditions[i].price > max_price_in_purchase_range:
                    max_price_in_purchase_range = self.market_conditions[i].price
                    max_price_offset = i
                    best_market_condition = self.market_conditions[i]

            logging.debug(
                f"algorithm_least_purchases: Current price at {curr_offset:03d}={self.market_conditions[curr_offset].price:.04f}, "
                f"Range({purchase_range_min:03d}-{purchase_range_max-1:03d}) has max={max_price_in_purchase_range:.4f} "
                f"@ minute {max_price_offset:03d}"
            )

            if max_price_in_purchase_range > self.market_conditions[curr_offset].price:
                # Step D
                trade_point = TradePoint(
                    purchase_point=self.market_conditions[curr_offset],
                    sell_point=best_market_condition,
                )
                trade_points.append(trade_point)
                # Step E
                curr_offset = max_price_offset + 1
            else:
                # Step F
                curr_offset += 1

        return trade_points

    def algorithm_quick_purchases(self) -> List[TradePoint]:
        """
        Steps for the Quick Purchase algorithm.
        Step A) Starting with the very first minute M
        Step B) Determine the allowed sell time-window for that minute
        Step C) In that range find the first price (say at Minute M) that is greater than the price at the current minute
        Step D) If such price was found perform the trade i.e. buy at M and sell at N
        Step E) If the trade was performed, skip to the minute N+1 and goto Step B
        Step F) If Step C could not find a price and the trade was not performed, then continue with minute M+1, and goto Step B

        PRO:
        - Easy to understand
        - Easy to implement

        CONS:
        - This algorithm is inefficient at profit-making because it does not explore further better prices in the range
        - This algorithm could also be very slow-performing in the following case:
            If the prices are constantly or mostly declining then Step C would end up exploring consecutive
            overlapping time-ranges
        """
        logging.info("Running: Algorithm of quick purchases")
        trade_points: List[TradePoint] = []

        # Step A
        curr_offset = 0
        while curr_offset + self.min_hold < len(self.market_conditions):

            # Step B
            purchase_range_min, purchase_range_max = self.get_purchase_range(
                curr_offset=curr_offset,
                num_market_conditions=len(self.market_conditions),
            )

            # Step C
            first_greater_price_offset = 0
            sell_market_condition: MarketCondition
            for i in range(purchase_range_min, purchase_range_max):
                if (
                    self.market_conditions[i].price
                    > self.market_conditions[curr_offset].price
                ):
                    first_greater_price_offset = i
                    sell_market_condition = self.market_conditions[i]
                    break

            if first_greater_price_offset:
                logging.debug(
                    f"algorithm_quick_purchases: Current price at {curr_offset:03d}={self.market_conditions[curr_offset].price:.04f}, "
                    f"Range({purchase_range_min:03d}-{purchase_range_max-1:03d}) has first greater={sell_market_condition.price:.4f} "
                    f"@ minute {first_greater_price_offset:03d}"
                )
                # Step D
                trade_point = TradePoint(
                    purchase_point=self.market_conditions[curr_offset],
                    sell_point=sell_market_condition,
                )
                trade_points.append(trade_point)
                # Step E
                curr_offset = first_greater_price_offset + 1
            else:
                # Step F
                logging.debug(
                    f"algorithm_quick_purchases: Current price at {curr_offset:03d}={self.market_conditions[curr_offset].price:.04f}, "
                    f"could not find next greater price in the Range({purchase_range_min:03d}-{purchase_range_max:03d})"
                )
                curr_offset += 1

        return trade_points

    def algorithm_most_purchases(self) -> List[TradePoint]:
        # TODO: This algorithm is incomplete (does not honor the max hold limit).
        #       The current implement is too complex to read and understand.
        #       Can be re-implemented.
        logging.info("Running: Algorithm of most purchases")
        trade_points: List[TradePoint] = []
        prev_offset = 0
        step = self.min_hold
        market_condition_prev: Any = self.market_conditions[prev_offset]
        market_condition_curr: Any = self.market_conditions[
            prev_offset + step
        ]  # TODO: boundary check
        potent_purchase_point = None
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
                    trade_point = TradePoint(
                        purchase_point=potent_purchase_point,
                        sell_point=market_condition_prev,
                    )
                    trade_points.append(trade_point)
                    potent_purchase_point = None
                    step = self.min_hold
                prev_offset += 1

            market_condition_prev = (
                self.market_conditions[prev_offset]
                if prev_offset < len(self.market_conditions)
                else None
            )
            market_condition_curr = (
                self.market_conditions[prev_offset + step]
                if (prev_offset + step) < len(self.market_conditions)
                else None
            )
            # logging.debug(f"{market_condition_prev=} {market_condition_curr=}")

        return trade_points

    def algorithm_new_unimplemented(self) -> List[TradePoint]:
        logging.info("algorithm_new_unimplemented")
        print("This algorithm is not yet implemented")
        trade_points: List[TradePoint] = []
        return trade_points
