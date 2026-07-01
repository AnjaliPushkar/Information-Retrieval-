"""
search.py
Basic Boolean retrieval using a linear scan over a document collection.
Returns (score, document) tuples — score is 1 for a match, 0 otherwise.
"""

import re
from document import Document


def linear_boolean_search(
    term: str,
    collection: list[Document],
    stopword_filtered: bool = False,
) -> list[tuple[int, Document]]:
    """
    Search *collection* for documents containing *term*.

    Parameters
    ----------
    term              : Single search term (case-insensitive).
    collection        : List of Document objects to scan.
    stopword_filtered : If True, search doc._filtered_terms instead of doc.terms.
                        Note: _filtered_terms is populated either by the stopword
                        removal functions (via test_wrapper) OR by direct assignment
                        doc.filtered_terms = [...] (as done in test_pr02_t3).

    Returns
    -------
    List of (score, Document) tuples for every document.
    Score = 1 if the document contains the term, 0 otherwise.
    Matching documents appear first (score=1), then non-matching (score=0).
    """
    normalized = _normalize_term(term)

    results: list[tuple[int, Document]] = []
    for doc in collection:
        # Always read from _filtered_terms when stopword_filtered=True.
        # _filtered_terms is set either via doc.filtered_terms = [...]
        # (intercepted by __setattr__) or via doc._filtered_terms = [...].
        term_list = doc._filtered_terms if stopword_filtered else doc.terms
        score = 1 if _contains(normalized, term_list) else 0
        results.append((score, doc))

    # Matching documents first, stable order preserved within each group
    results.sort(key=lambda pair: pair[0], reverse=True)
    return results



# Internal helpers
def _normalize_term(term: str) -> str:
    """Lowercase + apostrophe-aware clean — mirrors tokenize() in parser.py."""
    term = term.strip().lower()
    match = re.fullmatch(r"[a-z0-9]+(?:'[a-z]+)*", term)
    return match.group(0) if match else ""


def _contains(term: str, term_list: list) -> bool:
    """O(1) membership check — lowercases every term before comparing."""
    if not term:
        return False
    term_set = {t.lower() for t in term_list}
    return term in term_set