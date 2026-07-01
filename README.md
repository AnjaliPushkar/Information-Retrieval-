# Information-Retrieval
# Information Retrieval System — PR02

A command-line Information Retrieval (IR) system implemented in Python.

The system allows you to:

- Load a text collection from a URL (e.g., Project Gutenberg books)
- Perform Boolean keyword search
- Apply stop-word removal
  - List-based stop-word removal
  - Frequency-based stop-word removal (Crouch's method)
- Display loaded documents

---

# Running the Project

## Run the program

```bash
python main.py
```

If your system uses Python 3:

```bash
python3 main.py
```

You should see:

```
=== Information Retrieval System — PR02 ===
```

---

# Main Menu

```
1  Load collection from URL
2  Search (Boolean keyword)
3  Apply stop word removal
4  Show loaded documents
0  Exit
```

---

# Option 1 — Load Collection

Choose

```
1
```

You will be asked for:

### URL to the text file

Example:

```
https://www.gutenberg.org/cache/epub/78991/pg78991.txt
```

### Author name

Example:

```
Joseph Moxon
```

### Collection/book title

Example:

```
Moxon's Mechanick exercises, volume 2 (of 2)
```

### Start line

Example:

```
1
```

or

```
10
```

### End line

Example:

```
4000
```

### Regex pattern

Press **Enter** to use the default Gutenberg pattern.

After downloading you should see something similar to:

```
Downloading ...
Loaded 1 document(s).
```

---

# Option 2 — Boolean Search

Choose

```
2
```

Enter a keyword.

Example:

```
Search term:
Scholler
```

Then choose whether to search using filtered terms.

```
Search in stop-word-filtered terms? (y/n):
```

Examples:

```
n
```

or

```
y
```

Example output:

```
Found 1 matching document(s)
```

or

```
No documents matched.
```

---

# Option 3 — Stop Word Removal

Choose

```
3
```

Two methods are available.

---

## Method 1 — List-based

Choose

```
1
```

Enter the path to the stop-word file. (i.e. englishST.txt)

Example:

```
/Users/username/.../public_tests/englishST.txt
```

Example output:

```
Applied list-based removal (570 stop words)
```

The program also displays:

- number of terms before filtering
- number of terms after filtering
- number removed
- first 10 filtered terms

---

## Method 2 — Frequency-based (Crouch's Method)

Choose

```
2
```

Enter:

Common-frequency percentile

Example:

```
99
```

Rare-frequency percentile

Example:

```
1
```

Example output:

```
Applied Crouch removal (low=1%, high=99%)
```

You will also see:

- total terms before
- total terms after
- removed terms
- first 10 filtered terms

Example:

```
Before : 40858 terms
After  : 21740 terms
```

---

# Option 4 — Show Loaded Documents

Choose

```
4
```

Example output:

```
Collection: 1 document(s)

[0] MOXON'S MECHANICK EXERCISES
```

---

# Exit

Choose

```
0
```

Output:

```
Goodbye.
```
