import json
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.data_manager import data_manager, Dataset, SequenceFilter

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/datasets", response_model=List[Dataset])
async def get_datasets():
    return data_manager.get_datasets()


@app.post('/dataset')
async def set_dataset(sequenceFilter: SequenceFilter):
    print(sequenceFilter)
    return sequenceFilter
