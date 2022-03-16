import os
import warnings
import numpy as np

from difflib import SequenceMatcher
from joblib import dump, load
from sklearn.decomposition import PCA

from src.utils.common import NR_ATTR


def edit_cost(p1, p2):
    sequence_matcher = SequenceMatcher(None, p1, p2)
    matching_blocks = sequence_matcher.get_matching_blocks()
    ans = len(p1) + len(p2) - sum([m.size for m in matching_blocks]) * 2
    return ans


def normalize(coordinate, x_range=0.8, y_range=0.8):
    normalized_coordinate = np.empty(coordinate.shape)
    normalized_coordinate[:, 0] = (coordinate[:, 0] - coordinate[:, 0].min()) / \
                                  (coordinate[:, 0].max() - coordinate[:, 0].min()) * x_range + (1 - x_range) / 2
    normalized_coordinate[:, 1] = (coordinate[:, 1] - coordinate[:, 1].min()) / \
                                  (coordinate[:, 1].max() - coordinate[:, 1].min()) * y_range + (1 - y_range) / 2
    print(normalized_coordinate)
    return normalized_coordinate


class TacticDimensionalityReducer:
    def __init__(self):
        self.pca = None
        self.base_tactics = None

    def _get_mapping(self, tactics):
        tactics = [tactic["hits"] for tactic in tactics["patterns"]]
        base_tactics = [tactic["hits"] for tactic in self.base_tactics["patterns"]]
        mapping = [[0 for _ in base_tactics] for _ in tactics]
        for i in range(len(mapping)):
            for j in range(len(base_tactics)):
                mapping[i][j] = sum([edit_cost([hit[a_id] for hit in tactics[i]],
                                               [hit[a_id] for hit in base_tactics[j]])
                                     for a_id in range(NR_ATTR)])
        return mapping

    def fit(self, tactics, **kwargs):
        if len(tactics['patterns']) == 0:
            return []
        if self.pca is not None:
            warnings.warn("Overwriting exist pca model...")
        self.pca = PCA(n_components=2, random_state=7, **kwargs)
        self.base_tactics = tactics
        mapping = self._get_mapping(tactics)
        self.pca.fit(np.array(mapping))

    def transform(self, tactics):
        if len(tactics['patterns']) == 0:
            return []
        if self.pca is None:
            raise RuntimeError("No model fitted before transform.")
        mapping = self._get_mapping(tactics)
        return normalize(self.pca.transform(np.array(mapping))).tolist()

    def fit_transform(self, tactics, **kwargs):
        if len(tactics['patterns']) == 0:
            return []
        if self.pca is not None:
            warnings.warn("Overwriting exist pca model...")
        self.pca = PCA(n_components=2, random_state=7, **kwargs)
        self.base_tactics = tactics
        mapping = self._get_mapping(tactics)
        return normalize(self.pca.fit_transform(np.array(mapping))).tolist()

    def save(self, out_dir):
        pca_path = os.path.join(out_dir, 'tactic_dim_reducer.bin')
        base_tactics_path = os.path.join(out_dir, 'tactic_dim_reducer_base_tactics.bin')
        if not os.path.isfile(pca_path) and self.pca is not None:
            print('no standard scaler found. Saving it...')
            dump(self.pca, pca_path, compress=True)
            dump(self.base_tactics, base_tactics_path, compress=True)

    @classmethod
    def load(cls, out_dir):
        pca_path = os.path.join(out_dir, 'tactic_dim_reducer.bin')
        base_tactics_path = os.path.join(out_dir, 'tactic_dim_reducer_base_tactics.bin')
        model = cls()
        if os.path.isfile(pca_path):
            model.pca = load(pca_path)
        if os.path.isfile(base_tactics_path):
            model.base_tactics = load(base_tactics_path)
        return model
