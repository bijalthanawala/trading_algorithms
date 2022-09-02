from typing import Union
from market_condition import MarketCondition


class TradePoint:
    UNDETERMINED: float = float("inf")

    def __init__(self, purchase_point: MarketCondition):
        self.purchase_point: MarketCondition
        self.sell_point: Union[MarketCondition, None]

        self.purchase_point = purchase_point
        self.sell_point = None

    def sell_point_determined(self, sell_point: MarketCondition):
        self.sell_point = sell_point

    def __repr__(self):
        return f"Purchase@{self.purchase_point} Sell@{self.sell_point} Profit={self.profit} Duration={self.duration_held}"

    @property
    def profit(self):
        difference: float = self.UNDETERMINED
        if self.sell_point:
            difference = self.sell_point.price - self.purchase_point.price
        return difference

    @property
    def duration_held(self):
        difference: float = self.UNDETERMINED
        if self.sell_point:
            difference = self.sell_point.minute - self.purchase_point.minute
        return difference
