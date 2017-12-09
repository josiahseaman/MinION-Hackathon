import csv
from collections import OrderedDict


def _add_parent_rows(rows):
    parents_seen = set()
    new_rows = []
    for row in rows:
        parts = row[0].split('.')
        for i, level in enumerate(parts):
            path = '.'.join(parts[:i+1])
            if path not in parents_seen:
                parents_seen.add(path)
                if i == len(parts) - 1:
                    new_rows.append(row)
                else:
                    new_rows.append([path, ''])
    return new_rows
# Test: _add_parent_rows(rows)


def add_parents(input_path, output_path, row_limit=None):
    with open(input_path, 'r') as csvfile:
        f = csv.reader(csvfile)
        rows = []
        for row in f:
            # if ' ' not in row[0].split('.')[-1]:  # only species
            rows.append([part for part in row] )
        rows.sort(key=lambda x: x[0])
        # rows = rows[1:]  # skip first

    if row_limit is None:
        row_limit = len(rows)
    new_rows = _add_parent_rows(rows[:row_limit])

    with open(output_path, 'w') as out:
        out.write('id,value\n')
        for row in new_rows:
            out.write(','.join(row) + '\n')
# Test: add_parents('visualization/Treemap/flare-stripped.csv', 'visualization/Treemap/augmented-flare.csv')


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python preprocess_treemap_csv.py INPUT_PATH OUTPUT_PATH")
        print("Adds parent entries in the hierarchy")
        print("Example: python preprocess_treemap_csv.py flare-stripped.csv augmented-flare.csv")
        print("You'll need to process the input csv file into something treemap can read using this program."
              " Point the treemap website at the output of this script OUTPUT_PATH")
    add_parents(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else None)

r"""Running with:
python preprocess_treemap_csv.py ..\horrible_ncbi_taxonomy\temporary_taxonomy_list.csv "D:\josiah\Projects\DDV\build\www-data\dnadata\Treemap\flare.csv"
"""