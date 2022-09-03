from dataclasses import dataclass
from typing import Any


@dataclass
class Result:
    isSuccess: bool
    message: str
    result: Any
