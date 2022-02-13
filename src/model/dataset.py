from typing import List, Tuple
from pydantic import BaseModel


class MatchInfo(BaseModel):
    name: str
    players: Tuple[str, str]
    sequenceCount: int


class DatasetInfo(BaseModel):
    name: str
    matches: List[MatchInfo]


class SequenceFilter(BaseModel):
    dataset: str
    player: str
    opponents: List[str]
