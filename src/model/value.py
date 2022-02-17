from typing import Tuple, Dict

from pydantic import BaseModel


class Value(BaseModel):
    num_value: int
    name: str


class Freq(BaseModel):
    num_value: int
    freq: int


FreqValue = Dict[str, Freq]  # {name: (num_value, freq)}
