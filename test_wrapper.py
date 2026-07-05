from document import Document
from re import Pattern


# ----------------
# PR03 — Stemming
# ---------
def stem_term(term: str) -> str:
    """
    Stem a single term using the Porter stemming algorithm.
    Returns the stemmed string (always lowercase).

    Called directly by test_pr03_t1:
        stemmed_term = stem_term('koala')
    """
    from stemmer import stem_term as _stem
    return _stem(term)


# ------
# PR02 — Boolean search (extended with stemmed parameter for PR03)
# -------------------
def linear_boolean_search(
    term: str,
    collection: list[Document],
    stopword_filtered: bool = False,
    stemmed: bool = False,
) -> list[tuple[int, Document]]:
    """
    Search collection for documents containing term.
    Returns list of (score, Document) — score 1 = match, 0 = no match.
    Matching documents appear first.

    Parameters
    ----------
    stopword_filtered : If True, searches doc._filtered_terms.
    stemmed           : If True, stems both query and document terms
                        before matching (Porter algorithm).
    """
    from search import linear_boolean_search as _search
    return _search(term, collection, stopword_filtered, stemmed)


# ----
# PR02 — Stop word removal
# ---------------

def remove_stopwords_by_list(doc: Document, stopwords: set[str]):
    """
    Filter doc.terms against stopwords and store in doc._filtered_terms.
    Access result via doc.filtered_terms().
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
    Crouch frequency-based stop word removal.
    Stores result in doc._filtered_terms (access via doc.filtered_terms()).

    common_frequency : upper percentile — too common → stop word.
    rare_frequency   : lower percentile — too rare   → stop word.
    """
    from stopwords import remove_stop_words_by_frequency
    doc._filtered_terms = remove_stop_words_by_frequency(
        doc.terms,
        collection,
        low_freq=rare_frequency,
        high_freq=common_frequency,
    )


# ---------
# PR02 — Document loading
# ----

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
        url, search_pattern, start_line, end_line, author, origin,
    )