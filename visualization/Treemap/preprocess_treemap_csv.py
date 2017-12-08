import csv
from collections import OrderedDict


def _add_parent_rows(rows):
    parents_seen = set()
    new_rows = []
    for row in rows:
        parts = row['id'].split('.')[:-1]
        for i, level in enumerate(parts):
            path = '.'.join(parts[:i+1])
            if path not in parents_seen:
                parents_seen.add(path)
                new_rows.append(OrderedDict({'id':path,'value':''}))
        new_rows.append(row)
    return new_rows
# Test: _add_parent_rows(rows)


def add_parents(input_path, output_path):
    with open(input_path, 'r') as csvfile:
        f = csv.DictReader(csvfile)
        rows = [row for row in f][1:]  # skip first

    new_rows = _add_parent_rows(rows)

    with open(output_path, 'w') as out:
        out.write('id,value\n')
        for row in new_rows:
            out.write(row['id'] + ',' + row['value'] + '\n')
# Test: add_parents('visualization/Treemap/flare-stripped.csv', 'visualization/Treemap/augmented-flare.csv')


if __name__ == '__main__':
    import sys
    if len(sys.argv)  != 3:
        print("Usage: python preprocess input_path output_path")
        print("Adds parent entries in the hiearchy")
    add_parents(sys.argv[1], sys.argv[2])
