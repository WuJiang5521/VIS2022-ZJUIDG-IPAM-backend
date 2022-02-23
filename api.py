from typing import List, Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse, JSONResponse

from src.data_manager import data_manager
from src.model import DatasetInfo, SequenceFilter, TacticSet, Rally, Modification
from src.model.rally import RallyDetail
from src.utils import gen_token, video_file
from src.utils.token import auth_required, get_token_from_request

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 0. 确认后端运行状态
@app.get("/")
async def root():
    return {"message": "Hello World"}


# 1. 申请token
@app.get('/token', response_model=str)
async def get_token():
    token = gen_token()
    # TODO：可能需要在这里根据token初始化一些数据结构
    return token


# 2. 获取数据集列表
@app.get("/datasets", response_model=List[DatasetInfo])
async def get_datasets():
    return data_manager.get_datasets()


# 3. 指定数据集
@app.post('/dataset', response_model=bool)
@auth_required
async def set_dataset(request: Request, sequence_filter: SequenceFilter):
    token = get_token_from_request(request)
    # TODO: filter dataset and store it with token
    return True


# 4. 运算
@app.post('/tactic', response_model=TacticSet)
@auth_required
async def cal_tactic(request: Request):
    token = get_token_from_request(request)
    # TODO: calculate tactics
    tactics = {
        'tactics': [],
        'desc_len': 0,
    }
    return tactics


# 5. 获取回合
@app.get('/rally/{tac_id}', response_model=List[Rally])
@auth_required
async def get_rally(request: Request, tac_id: str):
    token = get_token_from_request(request)
    # TODO: return rallies that used the tactic with id `tac_id`
    rallies = []
    return rallies


# 6. 获取回合细节
# @app.get('/rally/detail/{rally_id}', response_model=RallyDetail)
# @auth_required
# async def get_rally(request: Request, rally_id: int):
#     token = get_token_from_request(request)
#     # TODO: return rallies that used the tactic with id `tac_id`
#     detail = {
#         "attr": [],
#         "hits": [],
#     }
#     return detail


# 7. 文本处理
@app.get('/text/{t}', response_model=Optional[Modification])
@auth_required
async def process_text(request: Request, t: str):
    # TODO: 返回文本处理结果
    return None


# 8. 增加修改
@app.post('/modification', response_model=TacticSet)
@auth_required
async def cal_tactic(request: Request, modication: Modification):
    token = get_token_from_request(request)
    # TODO: calculate tactics
    tactics = []
    return tactics


# 9. 撤销修改
@app.delete('/modification', response_model=bool)
@auth_required
async def cal_tactic(request: Request):
    token = get_token_from_request(request)
    # TODO: undo
    return True


# 10. 是否固定战术
@app.put('/tactic/preference/{tac_id}', response_model=bool)
@auth_required
async def fix_tactic(request: Request, tac_id: str, preference: bool):
    token = get_token_from_request(request)
    # TODO: fix tactic (if prefer) or not (otherwise)
    return True


# 11. 视频
@app.get('/video/{video_name}')
def get_video(video_name: str):
    try:
        return StreamingResponse(video_file(video_name), media_type="video/mp4")
    except:
        return JSONResponse(
            status_code=404,
            content={"detail": "Video is not found"}
        )
