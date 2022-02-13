from typing import List

from pydantic import BaseModel


Hit = List[str]


class RallyDetail(BaseModel):
    attr: List[str]
    hits: List[Hit]


class Rally(BaseModel):
    id: int  # 唯一标识，直接用筛选出来的数据集中这个回合的序号就行
    win: bool  # 选定球员是不是赢了
    is_server: bool  # 选定球员是不是发球方
    hit_count: int  # 总共多少拍

    # 战术信息
    index: int  # 战术是从第几拍开始用的

    # 比赛信息，如果没有就随便填个
    match_name: str  # 比赛名
    video_name: str  # 比赛视频名
    start_time: float  # 回合开始时间
    end_time: float  # 回合结束时间
