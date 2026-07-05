"""
search.py
Boolean retrieval using a linear scan over a document collection.
Returns (score, document) tuples — score is 1 for a match, 0 otherwise.

PR03: optional stemmed=True mode using Porter stemmer.
When stemmed=True, only matching documents (score=1) are returned.
"""

import re
from document import Document
from stemmer import stem_term


def linear_boolean_search(
    term: str,
    collection: list[Document],
    stopword_filtered: bool = False,
    stemmed: bool = False,
) -> list[tuple[int, Document]]:
    normalized = _normalize_term(term)
    if stemmed and normalized:
        normalized = stem_term(normalized)

    results: list[tuple[int, Document]] = []

    for doc in collection:
        term_list = doc._filtered_terms if stopword_filtered else doc.terms
        score = 1 if _contains(normalized, term_list, stemmed) else 0

        if stemmed:
            # Test checks: result_ids == {matching doc ids only}
            if score == 1:
                results.append((score, doc))
        else:
            results.append((score, doc))

    if not stemmed:
        # Matching documents first, stable order within each group
        results.sort(key=lambda pair: pair[0], reverse=True)

    return results


# ---------------------
# Internal helpers
# ----------------

def _normalize_term(term: str) -> str:
    """Lowercase + apostrophe-aware clean — mirrors tokenize() in parser.py."""
    term = term.strip().lower()
    match = re.fullmatch(r"[a-z0-9]+(?:'[a-z]+)*", term)
    return match.group(0) if match else ""


def _contains(term: str, term_list: list, stemmed: bool = False) -> bool:
    """
    Check whether *term* appears in *term_list*.
    When stemmed=True, all terms are stemmed before the set is built.
    """
    if not term:
        return False
    if stemmed:
        term_set = {stem_term(t.lower()) for t in term_list}
    else:
        term_set = {t.lower() for t in term_list}
    return term in term_set