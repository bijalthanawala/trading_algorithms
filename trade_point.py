from typing import Union
from stock_price import StockPrice


class TradePoint:
    def __init__(self, purchase_point: StockPrice):
        self.purchase_point: StockPrice
        self.sell_point: Union[StockPrice, None]

        self.purchase_point = purchase_point
        self.sell_point = None

    def sell_point_determined(self, sell_point: StockPrice):
        self.sell_point = sell_point

    @property
    def profit(self):
        difference = -1
        if self.sell_point:
            difference = self.sell_point.price - self.purchase_point.price
        return difference

    @property
    def duration_held(self):
        difference = -1
        if self.sell_point:
            difference = self.sell_point.minute - self.purchase_point.minute
        return difference
