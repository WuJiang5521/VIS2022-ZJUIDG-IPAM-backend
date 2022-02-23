import os


class DataManager:
    def __init__(self):
        self.datasets_path = './datasets'
        self.datasets = []
        self.__reload_datasets()

    def __reload_dataset(self, folder):
        path = os.path.join(self.datasets_path, folder)
        matches = []
        attrs = []
        for file in os.listdir(path):
            # TODO: setup attrs
            attrs = ['Ball Height', 'Ball Position', 'Hit Technique']
            matches.append({
                'name': file.split('.')[0],
                'players': ('a', 'b'),
                'sequenceCount': 100,
            })
        return {
            "name": folder,
            "matches": matches,
            "attrs": attrs,
        }

    def __reload_datasets(self):
        for folder in os.listdir(self.datasets_path):
            if os.path.isdir(os.path.join(self.datasets_path, folder)):
                self.datasets.append(self.__reload_dataset(folder))

    def get_datasets(self):
        return self.datasets


data_manager = DataManager()
