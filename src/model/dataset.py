from typing import List, Tuple
from pydantic import BaseModel


class MatchInfo(BaseModel):
    name: str
    players: Tuple[str, str]
    sequenceCount: int


class DatasetInfo(BaseModel):
    name: str
    matches: List[MatchInfo]
    attrs: List[str]


class SequenceFilter(BaseModel):
    dataset: str
    player: str
    opponents: List[str]
