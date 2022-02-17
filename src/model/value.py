from typing import Tuple, Dict

from pydantic import BaseModel


class Value(BaseModel):
    attr: str
    num_value: int
    name: str


class FreqValue(BaseModel):
    attr: str
    value: Dict[str, Tuple[int, int]]  # {name: (num_value, freq)}
