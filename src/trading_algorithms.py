from typing import List, Dict, Tuple, Any
from collections import OrderedDict
import logging

from .result import Result
from .market_condition import MarketCondition
from .trade_point import TradePoint


class TradingAlgorithms:
    DEFAULT_MIN_HOLD_MINUTES: int = 30
    DEFAULT_MAX_HOLD_MINUTES: int = 60

    @classmethod
    def ALGORITHMS(cls) -> Dict:
        algorithms = OrderedDict()
        algorithms["highest"] = cls.algorithm_purchase_next_highest
        algorithms["higher"] = cls.algorithm_purchase_next_higher
        algorithms["max"] = cls.algorithm_purchase_max
        algorithms["new"] = cls.algorithm_new_unimplemented
        return algorithms

    @classmethod
    def ALGORITHMS_CHOICES(cls) -> Dict:
        algorithms = cls.ALGORITHMS()
        return OrderedDict(
            (algo_short_name, algo_method.__name__)
            for algo_short_name, algo_method in algorithms.items()
        )

    def __init__(
        self, market_conditions: List[MarketCondition], min_hold=-1, max_hold=-1
    ):

        # Accept caller-supplied min_hold and max_hold only if those are valid
        if (min_hold == max_hold) or (min_hold >= max_hold):
            min_hold = max_hold = -1

        self.min_hold: int = (
            min_hold if min_hold >= 0 else self.DEFAULT_MIN_HOLD_MINUTES
        )
        self.max_hold: int = (
            max_hold if max_hold >= 0 else self.DEFAULT_MAX_HOLD_MINUTES
        )
        self.market_conditions: List[MarketCondition] = market_conditions

        logging.debug(
            f"TradingAlgorithms: Min hold time={self.min_hold} Max hold time={self.max_hold=}"
        )
        logging.debug(
            f"TradingAlgorithms: Loading {len(market_conditions)} market conditions"
        )

    def run(self, algorithm_choice) -> List[TradePoint]:
        # TODO: Find better way to do this, so that we do not have call this method with 'self' explicitly
        return self.ALGORITHMS()[algorithm_choice](self)

    # Allow only kwargs and avoid possible errors
    def get_purchase_range(
        self, *, curr_offset: int, num_market_conditions: int
    ) -> Tuple[int, int]:
        purchase_range_min = curr_offset + self.min_hold + 1
        purchase_range_max = min(curr_offset + self.max_hold + 1, num_market_conditions)
        return (purchase_range_min, purchase_range_max)

    def algorithm_purchase_max(self) -> List[TradePoint]:
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
        logging.info("Running: Algorithm of purchasing always the max")
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
            # TODO: This part of finding maximum in a range can use some improvements
            #       by using some knowledge from previous iteration
            #       However, the profit-making ability of this particular algorithm
            #       is so low that this improvement is not justified
            for i in range(purchase_range_min, purchase_range_max):
                if self.market_conditions[i].price > max_price_in_purchase_range:
                    max_price_in_purchase_range = self.market_conditions[i].price
                    max_price_offset = i
                    best_market_condition = self.market_conditions[i]

            logging.debug(
                f"algorithm_purchase_max: Current price at {curr_offset:03d}={self.market_conditions[curr_offset].price:.04f}, "
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

    def algorithm_purchase_next_higher(self) -> List[TradePoint]:
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
        logging.info("Running: Algorithm of purchasing the very next higher")
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
                    f"algorithm_purchase_next_higher: Current price at {curr_offset:03d}={self.market_conditions[curr_offset].price:.04f}, "
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
                    f"algorithm_purchase_next_higher: Current price at {curr_offset:03d}={self.market_conditions[curr_offset].price:.04f}, "
                    f"could not find next greater price in the Range({purchase_range_min:03d}-{purchase_range_max:03d})"
                )
                curr_offset += 1

        return trade_points

    def algorithm_purchase_next_highest(self) -> List[TradePoint]:
        """
        Steps for the Quick Purchase algorithm.
        Step A) Starting with the very first minute M
        Step B) Determine the allowed sell time-window for that minute
        Step C) In that range find the first price (say at Minute M) that is greater than the price at the current minute
        Step D) If such price was found, continue scanning the prices as long they are increasing
        Step E) Once a lower price is found perform the trade at the higest encountered price (sat at minute N) so far
        Step F) If the trade was performed, skip to the minute N+1 and goto Step B
        Step G) If Step C could not find a price and the trade was not performed, then continue with minute M+1, and goto Step B

        PRO:
        - Easy to understand
        - Easy to implement
        - This algorithm strives at maximizing profit-making by exploring the better prices in the range

        CONS:
        - This profit-making strategy is still myopic
        """
        logging.info("Running: Algorithm of purchasing the local highest")
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
            local_max_price_offset = 0
            sell_market_condition: MarketCondition
            for i in range(purchase_range_min, purchase_range_max):
                if (
                    self.market_conditions[i].price
                    > self.market_conditions[curr_offset].price
                ):
                    local_max_price_offset = i
                    sell_market_condition = self.market_conditions[i]
                    break

            # Step D
            if local_max_price_offset:
                i = i + 1
                while i < purchase_range_max:
                    if (
                        self.market_conditions[i].price
                        >= self.market_conditions[i - 1].price
                    ):
                        local_max_price_offset = i
                        sell_market_condition = self.market_conditions[i]
                    else:
                        break
                    i += 1

                logging.debug(
                    f"algorithm_purchase_next_highest: Current price at {curr_offset:03d}={self.market_conditions[curr_offset].price:.04f}, "
                    f"Range({purchase_range_min:03d}-{purchase_range_max-1:03d}) has first greater={sell_market_condition.price:.4f} "
                    f"@ minute {local_max_price_offset:03d}"
                )
                # Step E
                trade_point = TradePoint(
                    purchase_point=self.market_conditions[curr_offset],
                    sell_point=sell_market_condition,
                )
                trade_points.append(trade_point)
                # Step F
                curr_offset = local_max_price_offset + 1
            else:
                # Step G
                logging.debug(
                    f"algorithm_purchase_next_highest: Current price at {curr_offset:03d}={self.market_conditions[curr_offset].price:.04f}, "
                    f"could not find next greater price in the Range({purchase_range_min:03d}-{purchase_range_max:03d})"
                )
                curr_offset += 1

        return trade_points

    def algorithm_new_unimplemented(self) -> List[TradePoint]:
        logging.info("algorithm_new_unimplemented")
        print("This algorithm is not yet implemented")
        trade_points: List[TradePoint] = []
        return trade_points
