import os
import random
from typing import List, Optional

import numpy as np
from gensim.models import KeyedVectors

from dictionary import Dictionary


class Model:

    def __init__(self, paths: List[str], tolerance: float, dictionary: Dictionary):
        self.paths = paths
        self.wvs = {
            os.path.basename(p): KeyedVectors.load_word2vec_format(p, binary=True, unicode_errors="ignore")
            for p in self.paths
        }
        self.tolerance = tolerance / 100.
        self.search_space: set[str] = set(dictionary["lemme"].unique().tolist())

    def get_candidate(self, word: str, score: float) -> Optional[str]:
        candidates = self.get_all_candidates(word, score)
        try:
            return random.choice(list(candidates))
        except IndexError:
            return None

    def get_all_candidates(self, word: str, score: float) -> set[str]:
        min_score, max_score = (score / 100. - self.tolerance, score / 100. + self.tolerance)
        candidates = []
        for m, wv in self.wvs.items():
            all_similarities = wv.most_similar(word, topn=None)
            candidates += [wv.index_to_key[idx]
                           for idx in np.where((all_similarities >= min_score) & (all_similarities <= max_score))[0]]
        self.update_search_space(candidates)
        return self.search_space

    def update_search_space(self, candidates: list[str]) -> None:
        self.search_space = self.search_space.intersection(candidates)
