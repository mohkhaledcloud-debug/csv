# csv-cleaner

A small command line tool that cleans messy CSV files using only the Python standard library.

## What it does

- Normalizes headers: `"  First   Name "` becomes `first_name`
- Trims cells and collapses repeated spaces
- Drops completely empty rows
- Drops duplicate rows (case-insensitive, so `Ali` and `ali` count as the same)
- Pads short rows and trims long rows so every row matches the header
- Handles the invisible BOM that Excel adds to the first header
- Prints a short report of what it removed

## Usage

```
python clean_csv.py input.csv output.csv
```

## Example

Input (`examples/messy.csv`):

```
  First   Name ,Email,Age
  Ali ,ALI@x.com, 30
Sara,sara@x.com,25
,,
ali,ali@x.com,30
Omar,omar@x.com
Leo,leo@x.com,40,extra
```

Run:

```
python clean_csv.py examples/messy.csv examples/cleaned.csv
```

Output (`examples/cleaned.csv`):

```
first_name,email,age
Ali,ALI@x.com,30
Sara,sara@x.com,25
Omar,omar@x.com,
Leo,leo@x.com,40
```

Terminal report:

```
Read 6 rows, wrote 4
  dropped empty rows: 1
  dropped duplicates: 1
```

## Requirements

Python 3.8 or newer. No third-party packages.
