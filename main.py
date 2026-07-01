import os
import re
from document import Document
from parser import load_collection_from_url
from search import linear_boolean_search
from stopwords import load_stopword_list, remove_stop_words, remove_stop_words_by_frequency

# Global state
collection: list[Document] = []
# Menu
def main() -> None:
    print("\n=== Information Retrieval System — PR02 ===")
    while True:
        _print_menu()
        choice = input("Your choice: ").strip()
        if choice == "1":
            _handle_load_collection()
        elif choice == "2":
            _handle_search()
        elif choice == "3":
            _handle_stopword_removal()
        elif choice == "4":
            _handle_show_collection()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("  Unknown option — please enter a number from the menu.")


def _print_menu() -> None:
    loaded = f"{len(collection)} document(s) loaded" if collection else "no collection loaded"
    print(f"\n[{loaded}]")
    print("  1  Load collection from URL")
    print("  2  Search (Boolean keyword)")
    print("  3  Apply stop word removal")
    print("  4  Show loaded documents")
    print("  0  Exit")
# Menu handlers

def _handle_load_collection() -> None:
    global collection
    print("\n-- Load collection from URL --")
    url    = input("  URL to .txt file       : ").strip()
    author = input("  Author name            : ").strip()
    origin = input("  Collection/book title  : ").strip()

    try:
        start = int(input("  Start line (0-based)   : ").strip())
        end   = int(input("  End line   (0-based)   : ").strip())
    except ValueError:
        print("  ERROR: start/end must be integers.")
        return

    pattern_str = input(
        "  Regex pattern (group 1=title, group 2=body)\n"
        "  [leave blank for default Gutenberg pattern]: "
    ).strip()

    if not pattern_str:
        pattern_str = r"([A-Z][A-Z\s,'\-]{3,})\n\n([\s\S]+?)(?=\n[A-Z][A-Z\s,'\-]{3,}\n\n|\Z)"

    try:
        pattern = re.compile(pattern_str)
    except re.error as exc:
        print(f"  ERROR: invalid regex — {exc}")
        return

    print(f"  Downloading {url} …")
    try:
        collection = load_collection_from_url(url, pattern, start, end, author, origin)
    except Exception as exc:
        print(f"  ERROR: could not load collection — {exc}")
        return

    print(f"  Loaded {len(collection)} document(s).")


def _handle_search() -> None:
    if not collection:
        print("  No collection loaded — use option 1 first.")
        return

    print("\n-- Boolean keyword search --")
    term = input("  Search term: ").strip()
    if not term:
        print("  No term entered.")
        return

    use_filtered = _ask_yes_no("  Search in stop-word-filtered terms? (y/n): ")
    results = linear_boolean_search(term, collection, stopword_filtered=use_filtered)
    hits = [(score, doc) for score, doc in results if score == 1]

    print(f"\n  Found {len(hits)} matching document(s) for '{term}':")
    for score, doc in hits:
        print(f"    [{score}] ({doc.document_id}) {doc.title}")
    if not hits:
        print("  No documents matched.")


def _handle_stopword_removal() -> None:
    if not collection:
        print("  No collection loaded — use option 1 first.")
        return

    print("\n-- Stop word removal --")
    print("    1  List-based (load from file)")
    print("    2  Frequency-based (Crouch's method)")
    method = input("  Choose method (1/2): ").strip()

    if method == "1":
        _apply_list_based_removal()
    elif method == "2":
        _apply_frequency_based_removal()
    else:
        print("  Unknown method.")


def _apply_list_based_removal() -> None:
    filepath = input("  Path to stop word file: ").strip()
    if not os.path.isfile(filepath):
        print(f"  ERROR: file not found — {filepath}")
        return
    try:
        stopwords = load_stopword_list(filepath)
    except Exception as exc:
        print(f"  ERROR: could not load stop words — {exc}")
        return

    for doc in collection:
        doc._filtered_terms = remove_stop_words(doc.terms, stopwords)

    print(f"  Applied list-based removal ({len(stopwords)} stop words) to {len(collection)} document(s).")
    _show_filtered_sample()


def _apply_frequency_based_removal() -> None:
    try:
        high = float(input("  Common-frequency percentile (e.g. 99): ").strip())
        low  = float(input("  Rare-frequency percentile  (e.g.  1): ").strip())
    except ValueError:
        print("  ERROR: percentiles must be numbers.")
        return

    for doc in collection:
        doc._filtered_terms = remove_stop_words_by_frequency(
            doc.terms, collection, low_freq=low, high_freq=high
        )

    print(f"  Applied Crouch removal (low={low}%, high={high}%) to {len(collection)} document(s).")
    _show_filtered_sample()


def _handle_show_collection() -> None:
    if not collection:
        print("  No collection loaded.")
        return
    print(f"\n  Collection: {len(collection)} document(s)")
    for doc in collection:
        print(f"    [{doc.document_id:>3}] {doc.title}  ({len(doc.terms)} terms)")

# Helpers 
def _ask_yes_no(prompt: str) -> bool:
    return input(prompt).strip().lower() in ("y", "yes")


def _show_filtered_sample() -> None:
    if not collection:
        return
    doc = collection[0]
    before = len(doc.terms)
    after  = len(doc.filtered_terms())   # method call
    print(f"\n  Sample — '{doc.title}':")
    print(f"    Before : {before} terms")
    print(f"    After  : {after} terms  ({before - after} removed)")
    print(f"    First 10 filtered: {doc.filtered_terms()[:10]}")

if __name__ == "__main__":
    main()