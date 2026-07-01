"""
stopwords.py
Two stop word removal strategies:
  1. List-based       — filters against a stop word file.
  2. Frequency-based  — Crouch's percentile method across a collection.

Both store their result in doc._filtered_terms (accessed via doc.filtered_terms()).
All processing is case-insensitive. Punctuation and line breaks are stripped.
Internal apostrophes in contractions are preserved.
Output terms are always lowercased (required by the tests).
"""

import re
import math
from document import Document

# 1. List-based stop word removal
def load_stopword_list(filepath: str) -> set[str]:
    """
    Load stop words from a plain-text file (one word per line).
    Returns a set of normalised lowercase stop words.
    Handles Windows \\r\\n line endings automatically.
    """
    stopwords: set[str] = set()
    with open(filepath, encoding="utf-8") as fh:
        for line in fh:
            word = _normalize_term(line)
            if word:
                stopwords.add(word)
    return stopwords


def remove_stop_words(terms: list[str], stopwords: set[str]) -> list[str]:
    """
    Filter *terms* against *stopwords* (case-insensitive).
    Returns a new lowercased list — does NOT modify input.

    Called by test_wrapper.remove_stopwords_by_list().
    The tests expect:
      - lowercased output tokens
      - doc.filtered_terms() returns the result
    """
    # Normalise the incoming stopword set (handles raw file lines with \\r etc.)
    normalized_sw = {_normalize_term(w) for w in stopwords}
    result = []
    for t in terms:
        norm = _normalize_term(t)
        if norm and norm not in normalized_sw:
            result.append(norm)   # always lowercase
    return result

# 2. Frequency-based stop word removal (J. C. Crouch's method)
def compute_term_frequencies(collection: list[Document]) -> dict[str, int]:
    """
    Count how often each normalised term occurs across the whole *collection*.
    Returns dict: term → total count.
    """
    freq: dict[str, int] = {}
    for doc in collection:
        for raw_term in doc.terms:
            term = _normalize_term(raw_term)
            if term:
                freq[term] = freq.get(term, 0) + 1
    return freq


def select_stopwords_crouch(
    freq: dict[str, int],
    low_freq: float,
    high_freq: float,
) -> set[str]:
    """
    Select stop words using Crouch's frequency-percentile method.

    Terms at or below *low_freq* percentile  → too rare   → stop word.
    Terms at or above *high_freq* percentile → too common → stop word.
    """
    if not freq:
        return set()
    sorted_counts = sorted(freq.values())
    lower_threshold = _percentile_value(sorted_counts, low_freq)
    upper_threshold = _percentile_value(sorted_counts, high_freq)
    return {
        term for term, count in freq.items()
        if count <= lower_threshold or count >= upper_threshold
    }


def remove_stop_words_by_frequency(
    terms: list[str],
    collection: list[Document],
    low_freq: float,
    high_freq: float,
) -> list[str]:
    """
    Compute Crouch stop words from *collection*, then filter *terms*.
    Returns a lowercased list (consistent with remove_stop_words).

    Called by test_wrapper.remove_stopwords_by_frequency().
    Parameters low_freq / high_freq map to rare_frequency / common_frequency
    in the test wrapper.
    """
    freq = compute_term_frequencies(collection)
    stopwords = select_stopwords_crouch(freq, low_freq, high_freq)
    result = []
    for t in terms:
        norm = _normalize_term(t)
        if norm and norm not in stopwords:
            result.append(norm)
    return result
# Internal helpers

def _normalize_term(term: str) -> str:
    """
    Lowercase, strip surrounding punctuation, preserve internal apostrophes.
    Returns "" if no letters remain. Handles \\r\\n line endings.
    """
    term = term.strip().lower()
    term = re.sub(r"^[^a-z0-9']+|[^a-z0-9']+$", "", term)
    return term if re.search(r"[a-z]", term) else ""


def _percentile_value(sorted_values: list[int], percentile: float) -> int:
    """
    Nearest-rank percentile — always returns an actual value from the data.
    Uses ceiling formula: rank = ceil(p/100 * n).
    """
    if not sorted_values:
        return 0
    rank = math.ceil(percentile / 100.0 * len(sorted_values))
    rank = max(1, min(rank, len(sorted_values)))
    return sorted_values[rank - 1]