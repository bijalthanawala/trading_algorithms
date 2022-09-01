from dataclasses import dataclass


@dataclass(frozen=True)
class StockPrice:
    minute: int
    price: str
