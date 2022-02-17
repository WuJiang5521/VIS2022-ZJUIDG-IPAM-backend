from typing import List, Dict, Tuple

from pydantic import BaseModel

from src.model.rally import Hit


class ProbValue(BaseModel):
    attr: str
    value: Dict[str, Tuple[int, float]]  # {name: (num_value, prob)}


ProbHit = List[ProbValue]


class TacticDetail(BaseModel):
    attr: List[str]
    hits: List[Hit]  # some attr may be omitted


class TacticDetailWithProbability(BaseModel):
    attr: List[str]
    hits: List[ProbHit]


class Tactic(BaseModel):
    # 唯一表示
    id: str  # gen by str(uuid4())

    # TODO: 具体战术
    tactic: TacticDetail  # 如果是数组，这里可以改成List[HitDetail]
    tactic_surrounding: TacticDetailWithProbability

    # 使用统计
    seq_count: int  # 多少个回合使用了该战术（如果一个回合多次使用，只记一次）
    win_seq_count: int  # 使用该战术的回合，多少个赢了（同上）
    usage_count: int  # 该战术用了多少次（如果一个回合多次使用，记多次）
    win_usage_count: int  # 使用该战术，多少次赢了（同上）

    # 投影，0~1
    x: float
    y: float


class TacticSet(BaseModel):
    tactics: List[Tactic]
    desc_len: int
