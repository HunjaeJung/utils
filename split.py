import argparse
import os


def split(filehandler, delimiter=',', row_limit=1000,
          output_name_template='output_%s.csv', output_path='.', keep_headers=1):
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='csv splitter')
    
    parser.add_argument(
        '-f', '--filename', help='target csv file name', required=True)

    parser.add_argument(
        '-limit', '--row_limit', help='max limit row numbers (default 1000)', required=False, type=int)

    parser.add_argument(
        '-head', '--keep_headers', help='keep headers (0 or 1)', required=False, type=int)

    options = parser.parse_args()

    f = open(options.filename, 'r')

    row_limit = 1000 if options.row_limit is None else options.row_limit
    keep_headers = 1 if options.keep_headers is None else options.keep_headers

    split(f, row_limit=row_limit, keep_headers=keep_headers)

