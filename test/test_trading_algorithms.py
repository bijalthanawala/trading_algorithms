from typing import List

import unittest
from src import trading_algorithms
from src import market_condition

from src.market_condition import MarketCondition
from src.trading_algorithms import TradingAlgorithms
from src.trade_point import TradePoint


class TestTradingAlgorithms(unittest.TestCase):
    def setUp(self):
        # print("setUp: entry")
        self.mk1: MarketCondition = MarketCondition(0, 1.005)
        self.mk2: MarketCondition = MarketCondition(1, 1.050)
        self.mk3: MarketCondition = MarketCondition(2, 1.009)
        self.mk4: MarketCondition = MarketCondition(3, 1.010)
        self.market_conditions: List[MarketCondition] = [
            self.mk1,
            self.mk2,
            self.mk3,
            self.mk4,
        ]

    def tearDown(self):
        # print("tearDown: entry")
        pass

    def test_trading_algorithm_least_purchase_min_hold_0(self):
        trading_algorithms = TradingAlgorithms(
            self.market_conditions, min_hold=0, max_hold=100
        )
        trade_points: List[TradePoint] = trading_algorithms.run("least")
        self.assertEqual(len(trade_points), 2)
        self.assertEqual(trade_points[0].sell_point.price, self.mk2.price)
        self.assertEqual(trade_points[1].sell_point.price, self.mk4.price)

    def test_trading_algorithm_least_purchase_min_hold_1(self):
        trading_algorithms = TradingAlgorithms(
            self.market_conditions, min_hold=1, max_hold=100
        )
        trade_points: List[TradePoint] = trading_algorithms.run("least")
        self.assertEqual(len(trade_points), 1)
        self.assertEqual(trade_points[0].sell_point.price, self.mk4.price)

    def test_trading_algorithm_least_purchase_min_hold_2(self):
        trading_algorithms = TradingAlgorithms(
            self.market_conditions, min_hold=2, max_hold=100
        )
        trade_points: List[TradePoint] = trading_algorithms.run("least")
        self.assertEqual(len(trade_points), 1)
        self.assertEqual(trade_points[0].sell_point.price, self.mk4.price)
