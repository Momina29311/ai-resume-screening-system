from typing import Dict, Any

from sentence_transformers import SentenceTransformer, util


_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = SentenceTransformer(_MODEL_NAME)


def compute_semantic_similarity(resume_text: str, job_text: str) -> float:
    """
    Compute semantic similarity between resume and job description.
    Returns a score in [0, 100].
    """
    if not resume_text or not job_text:
        return 0.0

    resume_emb = _model.encode(resume_text, convert_to_tensor=True)
    job_emb = _model.encode(job_text, convert_to_tensor=True)

    score_tensor = util.cos_sim(resume_emb, job_emb)
    score = float(score_tensor.item())  # 0–1
    return round(score * 100.0, 2)


def semantic_match_result(resume_text: str, job_text: str) -> Dict[str, Any]:
    """
    Return a dict with semantic score and a human-readable label.
    """
    score = compute_semantic_similarity(resume_text, job_text)

    if score >= 85:
        label = "Strong Semantic Match"
    elif score >= 60:
        label = "Moderate Semantic Match"
    else:
        label = "Weak Semantic Match"

    return {
        "semantic_score": score,
        "semantic_label": label,
    }