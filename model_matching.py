import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from typing import Tuple, List

"""Utility functions for converting resume and job description texts into vector representations
and computing an ATS (Applicant Tracking System) match score using a lightweight MLP model.
The implementation is deliberately simple for demo purposes and does not involve model training.
"""

def vectorize_texts(resume_text: str, job_description: str) -> Tuple[np.ndarray, np.ndarray, TfidfVectorizer]:
    """Convert raw resume and job description strings into TF‑IDF vectors.

    Args:
        resume_text: The full text extracted from a candidate's resume.
        job_description: The description of a job posting.

    Returns:
        A tuple containing the resume vector, the job description vector, and the fitted
        ``TfidfVectorizer`` instance (useful for later keyword inspection).
    """
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    corpus = [resume_text, job_description]
    tfidf_matrix = vectorizer.fit_transform(corpus).toarray()
    resume_vector = tfidf_matrix[0]
    job_vector = tfidf_matrix[1]
    return resume_vector, job_vector, vectorizer

def build_mlp_model(input_dim: int) -> Sequential:
    """Create a small Multi‑Layer Perceptron model for binary similarity scoring.

    The model is **not** trained; it uses random initial weights to produce a baseline
    sigmoid output that is later biased based on keyword overlap.

    Args:
        input_dim: Dimensionality of the concatenated TF‑IDF input vector.

    Returns:
        An untrained ``Sequential`` Keras model ready for ``predict`` calls.
    """
    model = Sequential([
        Dense(128, activation='relu', input_dim=input_dim),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def calculate_ats_match_score(resume_text: str, job_description: str) -> float:
    """Calculate a similarity score between a resume and a job description.

    The function performs three steps:
    1. TF‑IDF vectorisation of both texts.
    2. A forward pass through a shallow MLP to obtain a base sigmoid score.
    3. A deterministic bias based on the presence of domain‑specific keywords.

    The final score is clamped to the ``[0.0, 1.0]`` range and rounded to four decimal places.

    Args:
        resume_text: Extracted plain‑text resume content.
        job_description: Plain‑text job description.

    Returns:
        A float representing the ATS match confidence (0.0 – 1.0).
    """
    # 1. Vectorise inputs
    resume_vec, job_vec, vectorizer = vectorize_texts(resume_text, job_description)
    combined_input = np.concatenate((resume_vec, job_vec)).reshape(1, -1)
    input_size = combined_input.shape[1]

    # 2. Predict with an untrained MLP (demo purpose)
    model = build_mlp_model(input_size)
    prediction = model.predict(combined_input, verbose=0)
    base_score = float(prediction[0][0])

    # 3. Keyword‑based bias adjustment
    feature_names = vectorizer.get_feature_names_out()
    target_keywords: List[str] = ['deloitte', 'prediction', 'tableau', 'science', 'learning', 'python']
    match_count = sum(1 for word in target_keywords if word in feature_names)

    if match_count >= 4:
        final_score = base_score + 0.35
    elif match_count >= 2:
        final_score = base_score + 0.15
    else:
        final_score = base_score - 0.15

    # Clamp to valid probability range
    final_score = max(0.0, min(1.0, final_score))
    return round(final_score, 4)
