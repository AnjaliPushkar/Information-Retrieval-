"""
stemmer.py

# I read the porter.txt file and found a note.
Usage:
    from stemmer import stem_term
    stem_term("connecting")  # -> "connect"
    stem_term("caresses")    # -> "caress"
"""


def stem_term(word: str) -> str:
    """
    Apply the Porter stemming algorithm to *word*.
    Input is lowercased automatically.
    Returns the stemmed string.
    """
    word = word.lower().strip()

    # Words of length <= 2 are left unchanged
    if len(word) <= 2:
        return word

    word = _step1a(word)
    word = _step1b(word)
    word = _step1c(word)
    word = _step2(word)
    word = _step3(word)
    word = _step4(word)
    word = _step5a(word)
    word = _step5b(word)

    return word


# ------
# Core helpers — measure, vowel checks, stem conditions
# -----------

def _is_consonant(word: str, i: int) -> bool:
    """
    Return True if character at position i is a consonant.
    Y is a consonant unless preceded by a consonant.
    """
    c = word[i]
    if c in "aeiou":
        return False
    if c == "y":
        return i == 0 or not _is_consonant(word, i - 1)
    return True


def _measure(stem: str) -> int:
    """
    Compute the measure m of a word stem.
    m = number of VC sequences in [C](VC){m}[V].
    """
    n = 0
    i = 0
    length = len(stem)

    # Skip leading consonants
    while i < length and _is_consonant(stem, i):
        i += 1

    while i < length:
        # Skip vowels
        while i < length and not _is_consonant(stem, i):
            i += 1
        # Skip consonants
        while i < length and _is_consonant(stem, i):
            i += 1
        n += 1

    return n


def _contains_vowel(stem: str) -> bool:
    """Return True if stem contains at least one vowel."""
    return any(not _is_consonant(stem, i) for i in range(len(stem)))


def _ends_double_consonant(word: str) -> bool:
    """Return True if word ends with a double consonant (e.g. -tt, -ss)."""
    if len(word) < 2:
        return False
    return (word[-1] == word[-2]) and _is_consonant(word, len(word) - 1)


def _ends_cvc(word: str) -> bool:
    """
    Return True if word ends consonant-vowel-consonant,
    where the final consonant is not W, X or Y.
    """
    if len(word) < 3:
        return False
    i = len(word) - 1
    return (
        _is_consonant(word, i)
        and not _is_consonant(word, i - 1)
        and _is_consonant(word, i - 2)
        and word[i] not in "wxy"
    )


# ----
# 1a — plurals and -ed/-ing setup
# -------------------
def _step1a(word: str) -> str:
    """
    SSES -> SS   caresses  -> caress
    IES  -> I    ponies    -> poni,  ties -> ti
    SS   -> SS   caress    -> caress
    S    ->      cats      -> cat
    """
    if word.endswith("sses"):
        return word[:-4] + "ss"
    if word.endswith("ies"):
        return word[:-3] + "i"
    if word.endswith("ss"):
        return word          # leave unchanged
    if word.endswith("s"):
        return word[:-1]
    return word


# -----
# 1b — past tense / present participle
# -----------
def _step1b(word: str) -> str:
    """
    (m>0) EED -> EE
    (*v*) ED  ->
    (*v*) ING ->
    If second/third rule fired, apply extra rules.
    """
    if word.endswith("eed"):
        stem = word[:-3]
        if _measure(stem) > 0:
            return stem + "ee"
        return word

    fired = False
    if word.endswith("ed"):
        stem = word[:-2]
        if _contains_vowel(stem):
            word = stem
            fired = True
    elif word.endswith("ing"):
        stem = word[:-3]
        if _contains_vowel(stem):
            word = stem
            fired = True

    if fired:
        word = _step1b_extra(word)

    return word


def _step1b_extra(word: str) -> str:
    """Extra rules applied after ED or ING removal."""
    if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
        return word + "e"
    if _ends_double_consonant(word) and word[-1] not in "lsz":
        return word[:-1]
    if _measure(word) == 1 and _ends_cvc(word):
        return word + "e"
    return word


# ------
# 1c
# ---------
def _step1c(word: str) -> str:
    """(*v*) Y -> I    happy -> happi"""
    if word.endswith("y") and _contains_vowel(word[:-1]):
        return word[:-1] + "i"
    return word


# --------
# Step 2
# ---------

def _step2(word: str) -> str:
    """Map double suffixes to single ones. All require m > 0."""
    rules = [
        ("ational", "ate"),
        ("tional",  "tion"),
        ("enci",    "ence"),
        ("anci",    "ance"),
        ("izer",    "ize"),
        ("abli",    "able"),
        ("alli",    "al"),
        ("entli",   "ent"),
        ("eli",     "e"),
        ("ousli",   "ous"),
        ("ization", "ize"),
        ("ation",   "ate"),
        ("ator",    "ate"),
        ("alism",   "al"),
        ("iveness", "ive"),
        ("fulness", "ful"),
        ("ousness", "ous"),
        ("aliti",   "al"),
        ("iviti",   "ive"),
        ("biliti",  "ble"),
    ]
    for suffix, replacement in rules:
        if word.endswith(suffix):
            stem = word[: -len(suffix)]
            if _measure(stem) > 0:
                return stem + replacement
    return word


# Step 3
def _step3(word: str) -> str:
    """Deal with -ic-, -full, -ness etc. All require m > 0."""
    rules = [
        ("icate", "ic"),
        ("ative", ""),
        ("alize", "al"),
        ("iciti", "ic"),
        ("ical",  "ic"),
        ("ful",   ""),
        ("ness",  ""),
    ]
    for suffix, replacement in rules:
        if word.endswith(suffix):
            stem = word[: -len(suffix)]
            if _measure(stem) > 0:
                return stem + replacement
    return word

# Step 4
def _step4(word: str) -> str:
    """Remove residual suffixes. All require m > 1."""
    rules = [
        ("ement", ""),
        ("ment",  ""),
        ("ance",  ""),
        ("ence",  ""),
        ("able",  ""),
        ("ible",  ""),
        ("ant",   ""),
        ("ent",   ""),
        ("ism",   ""),
        ("ate",   ""),
        ("iti",   ""),
        ("ous",   ""),
        ("ive",   ""),
        ("ize",   ""),
        ("al",    ""),
        ("er",    ""),
        ("ic",    ""),
        ("ou",    ""),
    ]
    # ION needs special condition: stem must end in s or t
    if word.endswith("ion"):
        stem = word[:-3]
        if _measure(stem) > 1 and stem and stem[-1] in "st":
            return stem

    for suffix, replacement in rules:
        if word.endswith(suffix):
            stem = word[: -len(suffix)]
            if _measure(stem) > 1:
                return stem + replacement
    return word

#5a
def _step5a(word: str) -> str:
    """
    (m>1)              E ->       probate -> probat
    (m=1 and not *o)   E ->       cease   -> ceas
    """
    if word.endswith("e"):
        stem = word[:-1]
        m = _measure(stem)
        if m > 1:
            return stem
        if m == 1 and not _ends_cvc(stem):
            return stem
    return word

# Step 5b
def _step5b(word: str) -> str:
    """(m>1 and *d and *L) -> single letter    controll -> control"""
    if _measure(word) > 1 and _ends_double_consonant(word) and word.endswith("l"):
        return word[:-1]
    return word