from dataclasses import dataclass


@dataclass(frozen=True)
class MarketCondition:
    minute: int
    price: str
