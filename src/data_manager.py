import imp


import os
from typing import List, Tuple
from pydantic import BaseModel

class MatchInfo(BaseModel):
    name: str
    players: Tuple[str, str]
    sequenceCount: int

class Dataset(BaseModel):
    name: str
    matches: List[MatchInfo]

class SequenceFilter(BaseModel):
    dataset: str
    player: str
    opponents: List[str]

class DataManager:
    def __init__(self):
        self.datasets_path = './datasets'
        self.datasets = []
        self.__reload_datasets()

    def __reload_dataset(self, folder):
        path = os.path.join(self.datasets_path, folder)
        matches = []
        for file in os.listdir(path):
            matches.append({
                'name': file.split('.')[0],
                'players': ('a', 'b'),
                'sequenceCount': 100,
            })
        return {
            "name": folder,
            "matches": matches
        }

    def __reload_datasets(self):
        for folder in os.listdir(self.datasets_path):
            if os.path.isdir(os.path.join(self.datasets_path, folder)):
                self.datasets.append(self.__reload_dataset(folder))

    def get_datasets(self):
        return self.datasets

data_manager = DataManager()