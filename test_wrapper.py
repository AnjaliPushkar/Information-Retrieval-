# Information Retrieval - Practical Task 2
# Wrapper for Unit Tests
# Version 1.1 (2025-06-04)

from document import Document
from re import Pattern


def remove_stopwords_by_list(doc: Document, stopwords: set[str]):
    """
    Remove stopwords from the given document and store result in doc._filtered_terms.

    - Filters doc.terms against the provided stopword set (case-insensitive).
    - Output terms are lowercased.
    - Leaves doc.terms and doc.raw_text unchanged.
    - Access result via doc.filtered_terms()  (method call).
    """
    from stopwords import remove_stop_words
    doc._filtered_terms = remove_stop_words(doc.terms, stopwords)


def remove_stopwords_by_frequency(
    doc: Document,
    collection: list[Document],
    common_frequency: float,
    rare_frequency: float,
):
    """
    Remove stopwords using Crouch's frequency-percentile method.
    Stores result in doc._filtered_terms (access via doc.filtered_terms()).

    common_frequency : upper percentile — terms at/above this are too common.
    rare_frequency   : lower percentile — terms at/below this are too rare.
    """
    from stopwords import remove_stop_words_by_frequency
    doc._filtered_terms = remove_stop_words_by_frequency(
        doc.terms,
        collection,
        low_freq=rare_frequency,       # rare_frequency  → lower cut-off
        high_freq=common_frequency,    # common_frequency → upper cut-off
    )


def load_documents_from_url(
    url: str,
    author: str,
    origin: str,
    start_line: int,
    end_line: int,
    search_pattern: Pattern[str],
) -> list[Document]:
    """
    Download a .txt file and extract stories into Document objects.
    Uses search_pattern (group 1 = title, group 2 = body).
    Only lines [start_line : end_line] are considered.
    """
    from parser import load_collection_from_url
    return load_collection_from_url(
        url,
        search_pattern,
        start_line,
        end_line,
        author,
        origin,
    )


def linear_boolean_search(
    term: str,
    collection: list[Document],
    stopword_filtered: bool = False,
) -> list[tuple[int, Document]]:
    """
    Search collection for documents containing term.
    Returns list of (score, Document) — score 1 = match, 0 = no match.
    Matching documents appear first.
    If stopword_filtered=True, searches doc._filtered_terms instead of doc.terms.
    """
    from search import linear_boolean_search as _search
    return _search(term, collection, stopword_filtered)