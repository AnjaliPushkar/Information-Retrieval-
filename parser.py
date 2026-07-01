"""
parser.py
Downloads a plain-text story collection from a URL and extracts individual
Document objects using a regex pattern to locate titles and bodies.
"""

import re
import urllib.request
from document import Document


def tokenize(text: str) -> list[str]:
    """
    Split text into lowercase word tokens.
    Strips punctuation but preserves internal apostrophes so that
    contractions like "don't" remain a single token.
    """
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)*", text)


def load_collection_from_url(
    url: str,
    search_pattern: re.Pattern,
    start_line: int,
    end_line: int,
    author: str,
    origin: str,
) -> list[Document]:
    """
    Download a plain-text file and extract stories into Document objects.

    Parameters
    ----------
    url: Direct URL to a .txt file (e.g. from Project Gutenberg).
    search_pattern : Compiled regex whose group 1 = title, group 2 = body text.
    start_line: 0-based index of the first line to include (skips header).
    end_line: 0-based index of the last line to include (skips footer).
    author: Author name attached to every Document.
    origin : Source book/collection name attached to every Document.

    Returns
    -------
    List of Document objects ordered by position in the source file.
    """
    raw_bytes = _download(url)

    full_text = raw_bytes.decode("utf-8", errors="replace")
    lines = full_text.splitlines()
    working_text = "\n".join(lines[start_line:end_line])

    matches = list(search_pattern.finditer(working_text))

    documents: list[Document] = []
    for doc_id, match in enumerate(matches):
        title = match.group(1).strip()
        body  = match.group(2).strip()
        raw_text = re.sub(r"\s+", " ", body).strip()
        terms = tokenize(raw_text)

        documents.append(
            Document(
                document_id=doc_id,
                title=title,
                raw_text=raw_text,
                terms=terms,
                author=author,
                origin=origin,
            )
        )

    return documents


def _download(url: str) -> bytes:
    """Fetch raw bytes from *url* using the standard library only."""
    with urllib.request.urlopen(url) as response:
        return response.read()