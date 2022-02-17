from typing import List, Tuple

from pydantic import BaseModel


class Value(BaseModel):
    num_value: int  # id value used in alg
    name: str
    attr: str


Hit = List[Value]


class RallyDetail(BaseModel):
    attr: List[str]
    hits: List[Hit]


class Rally(BaseModel):
    id: int  # 唯一标识，直接用筛选出来的数据集中这个回合的序号就行
    win: bool  # 选定球员是不是赢了
    is_server: bool  # 选定球员是不是发球方
    hit_count: int  # 总共多少拍

    # 战术信息
    index: List[Tuple[int, int]]  # 战术是从第几拍开始用的 [(tactic_id, index_in_rally)]

    rally: RallyDetail

    # 比赛信息，如果没有就随便填个
    match_name: str  # 比赛名
    video_name: str  # 比赛视频名
    start_time: float  # 回合开始时间
    end_time: float  # 回合结束时间
