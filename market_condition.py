from dataclasses import dataclass


@dataclass(frozen=True)
class MarketCondition:
    minute: int
    price: str

    def __repr__(self):
        # return f"minute:{self.minute:03d} price:{self.price:.4f}"
        return f"{self.minute:03d}({self.price:.4f})"
