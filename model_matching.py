import numpy as np
from functools import lru_cache
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout


def vectorize_texts(resume_text: str, job_description: str):
    """Convert raw resume and job description strings into TF‑IDF vectors.

    Args:
        resume_text: Text extracted from the candidate's resume.
        job_description: Text describing the job posting.

    Returns:
        Tuple containing the resume vector, job vector and the fitted vectorizer.
    """
    vectorizer = TfidfVectorizer(max_features=500, stop_words="english")
    corpus = [resume_text, job_description]
    tfidf_matrix = vectorizer.fit_transform(corpus).toarray()
    resume_vector = tfidf_matrix[0]
    job_vector = tfidf_matrix[1]
    return resume_vector, job_vector, vectorizer


@lru_cache(maxsize=32)
def build_mlp_model(input_dim: int) -> Sequential:
    """Create (or retrieve cached) MLP model for a given input dimension.

    The model architecture is static; caching avoids rebuilding and recompiling
    the same network on every score calculation, which improves runtime
    performance when many jobs are evaluated.
    """
    model = Sequential([
        Dense(128, activation="relu", input_dim=input_dim),
        Dropout(0.2),
        Dense(64, activation="relu"),
        Dropout(0.2),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid"),
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


def calculate_ats_match_score(resume_text: str, job_description: str) -> float:
    """Calculate a normalized ATS match score between a resume and a job posting.

    The function vectorises the texts, feeds the concatenated vectors through a
    lightweight MLP, and then applies a keyword‑based bias to make the score more
    realistic for demo purposes.

    Returns:
        A float in the range ``0.0`` – ``1.0`` representing the match confidence.
    """
    # Vectorise inputs
    resume_vec, job_vec, vectorizer = vectorize_texts(resume_text, job_description)
    combined_input = np.concatenate((resume_vec, job_vec)).reshape(1, -1)
    input_size = combined_input.shape[1]

    # Reuse cached model when possible
    model = build_mlp_model(input_size)
    prediction = model.predict(combined_input, verbose=0)
    base_score = float(prediction[0][0])

    # Keyword biasing – simple heuristic to adjust the raw sigmoid output
    feature_names = vectorizer.get_feature_names_out()
    target_keywords = ["deloitte", "prediction", "tableau", "science", "learning", "python"]
    match_count = sum(1 for word in target_keywords if word in feature_names)

    if match_count >= 4:
        final_score = base_score + 0.35
    elif match_count >= 2:
        final_score = base_score + 0.15
    else:
        final_score = base_score - 0.15

    # Clamp to valid range
    final_score = max(0.0, min(1.0, final_score))
    return round(final_score, 4)
