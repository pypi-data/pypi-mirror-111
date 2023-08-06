"""Embedding utilities."""

from typing import List

import numpy as np

DOT = "dot"
COSINE = "cosine"


def compute_scores(query_embedding, item_embeddings, measure=DOT):
    """Computes the scores of the candidates given a query.

    Args:
      query_embedding: a vector of shape [k], representing the query embedding.
      item_embeddings: a matrix of shape [N, k], such that row i is the embedding
        of item i.
      measure: a string specifying the similarity measure to be used. Can be
        either DOT or COSINE.

    Returns:
      scores: a vector of shape [N], such that scores[i] is the score of item i.
    """
    u = query_embedding
    V = item_embeddings
    if measure == COSINE:
        V = V / np.linalg.norm(V, axis=1, keepdims=True)
        u = u / np.linalg.norm(u)
    scores = u.dot(V.T)
    return scores


def find_nearest_neighbors(
    query_embedding, item_embeddings, measure=COSINE, k=5
) -> List[int]:
    """Finds the indices of the neareast neighbors in embeddings.

    Args:
        query_embedding: a vector of shape [k], representing the query embedding.
        item_embeddings: a matrix of shape [N, k], such that row i is the embedding of
            item i.
        measure: a string specifying the similarity measure to be used. Can be
            either DOT or COSINE.
        k: number of nearest neighbors.

    Returns:
        A list of k indices of the nearest neighbors.

    NOTE: For large N, you might want to use approximate neareast neighbor algorithms
    instead.
    """
    distances = compute_scores(query_embedding, item_embeddings, measure=measure)
    return (-distances).argsort()[:k]
