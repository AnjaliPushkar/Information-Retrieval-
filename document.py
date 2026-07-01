"""
document.py
Defines the Document dataclass used throughout the IR system.

filtered_terms dual interface explanation:
  test_pr02_t3 assigns it as a plain attribute:  d1.filtered_terms = [...]
  test_pr02_t4 calls it as a method:             doc.filtered_terms()

  Solution: use a @property.
    - The setter stores the value in _filtered_terms.
    - The getter returns a _CallableList (a list that is also callable),
      so both  doc.filtered_terms  (returns list)  and
               doc.filtered_terms()  (calls the list → returns list)  work.
    - Pylance sees a normal property, so assignment is valid and no warning.
"""

from dataclasses import dataclass, field


class _CallableList(list):
    """
    A list subclass that is also callable.
    Calling an instance returns a plain list copy of itself.
    This makes  doc.filtered_terms()  work whether filtered_terms is
    accessed as a property (returning this object) or called directly.
    """
    def __call__(self) -> list:
        return list(self)


@dataclass
class Document:
    """A single story/chapter extracted from a text collection."""

    document_id: int
    title: str
    raw_text: str
    terms: list          = field(default_factory=list)
    author: str          = ""
    origin: str          = ""
    _filtered_terms: list = field(default_factory=_CallableList, repr=False)

    @property
    def filtered_terms(self) -> _CallableList:
        """
        Return the stop-word-filtered term list as a callable list.
        Usage:
            doc.filtered_terms          → _CallableList (iterable, sliceable)
            doc.filtered_terms()        → plain list copy  (test_pr02_t4)
            doc.filtered_terms = [...]  → stored via setter (test_pr02_t3)
        """
        if not isinstance(self._filtered_terms, _CallableList):
            # Ensure it's always a _CallableList even if set via _filtered_terms directly
            object.__setattr__(self, "_filtered_terms", _CallableList(self._filtered_terms))
        return self._filtered_terms   # type: ignore[return-value]

    @filtered_terms.setter
    def filtered_terms(self, value: list) -> None:
        """
        Allow  doc.filtered_terms = [...]  as a plain attribute assignment.
        Wraps value in _CallableList so the getter always returns a callable.
        """
        object.__setattr__(self, "_filtered_terms", _CallableList(value))

    def __repr__(self) -> str:
        preview = self.raw_text[:60].replace("\n", " ")
        return (
            f"Document(id={self.document_id}, title={self.title!r}, "
            f"terms={len(self.terms)}, preview={preview!r}...)"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Document):
            return NotImplemented
        return self.document_id == other.document_id

    def __hash__(self) -> int:
        return hash(self.document_id)