import logging

from typing import List, Tuple, Union
from market_condition import MarketCondition


class StockPrices:
    def __init__(self, market_conditions: List[MarketCondition]):
        self.market_conditions: List[MarketCondition] = market_conditions
