from typing import List, Tuple, Union

from pydantic import BaseModel

from src.model.hit import HitWithoutFrequency, HitWithFrequency


class Tactic(BaseModel):
    # 唯一表示
    id: str  # gen by str(uuid4())

    # 具体战术
    user: int  # tactic第一拍的击球方，0或1
    tactic: List[HitWithoutFrequency]  # 如果是数组，这里可以改成List[HitDetail]
    tactic_surrounding: List[HitWithFrequency]

    # 使用统计
    seq_count: int  # 多少个回合使用了该战术（如果一个回合多次使用，只记一次）
    win_seq_count: int  # 使用该战术的回合，多少个赢了（同上）
    usage_count: int  # 该战术用了多少次（如果一个回合多次使用，记多次）
    win_usage_count: int  # 使用该战术，多少次赢了（同上）

    # 投影，0~1
    x: float
    y: float

    # 回合序号
    index: List[Tuple[int, List[int]]]  # [(rally_id, index_in_rally)] or [(rally_id, [index_in_rally])]


class TacticSet(BaseModel):
    tactics: List[Tactic]
    desc_len: int
