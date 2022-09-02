from dataclasses import dataclass


@dataclass(frozen=True)
class MarketCondition:
    minute: int
    price: str

    def __repr__(self):
        return f"{self.minute:05d}({self.price:.4f})"
