import csv
import sys


def main():
    # Expect exactly two arguments after the script name: input and output paths
    if len(sys.argv) != 3:
        sys.exit("Usage: python clean_csv.py input.csv output.csv")

    # Pipeline: read -> clean -> write
    rows, stats = clean(read_rows(sys.argv[1]))
    write_rows(sys.argv[2], rows)

    # rows includes the header, so subtract 1 for the data-row count
    print(f"Read {stats['read']} rows, wrote {len(rows) - 1}")
    print(f"  dropped empty rows: {stats['empty']}")
    print(f"  dropped duplicates: {stats['duplicates']}")


def read_rows(path):
    try:
        # newline="" is what the csv module requires so it handles line endings itself
        # utf-8-sig silently strips the invisible BOM that Excel adds to the first header
        with open(path, newline="", encoding="utf-8-sig") as file:
            return list(csv.reader(file))  # list of lists of strings
    except FileNotFoundError:
        sys.exit(f"File not found: {path}")


def write_rows(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as file:
        csv.writer(file).writerows(rows)


def clean(rows):
    # Counters so the user can see what was removed
    stats = {"read": max(len(rows) - 1, 0), "empty": 0, "duplicates": 0}
    if not rows:  # completely empty file: nothing to clean
        return rows, stats

    # First row is the header; normalize it once
    header = [clean_header(h) for h in rows[0]]
    width = len(header)
    seen = set()  # fingerprints of rows already kept, for duplicate detection
    cleaned = [header]

    for row in rows[1:]:
        # split() with no argument splits on any whitespace run and drops the
        # ends, so " ".join(...) trims the cell and collapses inner spaces
        row = [" ".join(cell.split()) for cell in row]
        # Pad short rows with "" and cut long ones so every row matches the header
        row = (row + [""] * width)[:width]

        # any(row) is False only when every cell is "" -> a blank row
        if not any(row):
            stats["empty"] += 1
            continue

        # Lowercase so "Ali" and "ali" count as duplicates; tuple so it can go in a set
        key = tuple(cell.lower() for cell in row)
        if key in seen:
            stats["duplicates"] += 1
            continue
        seen.add(key)
        cleaned.append(row)  # keep the original casing, not the lowercase key

    return cleaned, stats


def clean_header(name):
    # "  First   Name " -> "first_name"
    return "_".join(name.lower().split())


if __name__ == "__main__":
    main()
