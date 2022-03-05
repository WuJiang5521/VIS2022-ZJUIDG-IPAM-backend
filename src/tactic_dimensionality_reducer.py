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


class TacticDimensionalityReducer:
    def __init__(self):
        self.pca = None

    @staticmethod
    def _get_mapping(tactics):
        tactics = [tactic["hits"] for tactic in tactics["patterns"]]
        mapping = [[0 for _ in tactics] for _ in tactics]
        for i in range(len(mapping)):
            for j in range(i + 1, len(mapping)):
                mapping[i][j] = sum([edit_cost([hit[a_id] for hit in tactics[i]],
                                               [hit[a_id] for hit in tactics[j]])
                                     for a_id in range(NR_ATTR)])
        for i in range(len(mapping)):
            for j in range(i):
                mapping[i][j] = mapping[j][i]
        return mapping

    def fit(self, tactics, **kwargs):
        if self.pca is not None:
            warnings.warn("Overwriting exist pca model...")
        self.pca = PCA(n_components=2, random_state=7, **kwargs)
        mapping = TacticDimensionalityReducer._get_mapping(tactics)
        self.pca.fit(np.array(mapping))

    def transform(self, tactics):
        if self.pca is None:
            raise RuntimeError("No model fitted before transform.")
        mapping = TacticDimensionalityReducer._get_mapping(tactics)
        return self.pca.transform(np.array(mapping)).tolist()

    def fit_transform(self, tactics, **kwargs):
        if self.pca is not None:
            warnings.warn("Overwriting exist pca model...")
        self.pca = PCA(n_components=2, random_state=7, **kwargs)
        mapping = TacticDimensionalityReducer._get_mapping(tactics)
        return self.pca.fit_transform(np.array(mapping)).tolist()

    def save(self, out_dir):
        pca_path = os.path.join(out_dir, 'tactic_dim_reducer.bin')
        if not os.path.isfile(pca_path) and self.pca is not None:
            print('no standard scaler found. Saving it...')
            dump(self.pca, pca_path, compress=True)

    @classmethod
    def load(cls, out_dir):
        pca_path = os.path.join(out_dir, 'tactic_dim_reducer.bin')
        model = cls()
        if os.path.isfile(pca_path):
            model.pca = load(pca_path)
        return model
