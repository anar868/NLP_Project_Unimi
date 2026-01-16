import numpy as np

def compute_alignment_scores(scope_emb: np.ndarray, abs_embs: np.ndarray) -> np.ndarray:
    return abs_embs @ scope_emb[0]

def top_bottom(df, k=5):
    top = df.sort_values("alignment_score", ascending=False).head(k)
    bottom = df.sort_values("alignment_score", ascending=True).head(k)
    return top, bottom