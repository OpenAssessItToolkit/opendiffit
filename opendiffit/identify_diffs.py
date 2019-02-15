import csv
import os
import argparse
import logging
from utils import initialize_logger
from utils import check_header


def get_args():
    example_text = '''
    examples:

    python opendiffit/%(identify_diffs)s --old="old-report.csv" --new="new-report.csv" --diff="diff-report.csv"

    ''' % {'identify_diffs': os.path.basename(__file__)}

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-o', '--old', help='original csv')
    parser.add_argument('-n', '--new', help='new csv')
    parser.add_argument('-d', '--diff', help='output csv')
    return parser.parse_args()

def identify_diffs(old, new, diff):
    """ Identify rows with changed cells """
    with open(old, 'r', encoding='utf-8-sig') as r_csv_old, \
        open(new, 'r', encoding='utf-8-sig') as r_csv_new, \
        open(diff, 'w', encoding='utf-8-sig') as w_csv_diff:

        reader_old = csv.DictReader(r_csv_old)
        reader_new = csv.DictReader(r_csv_new)
        fieldnames = reader_new.fieldnames + ['diff']
        writer = csv.DictWriter(w_csv_diff, fieldnames=fieldnames)
        writer.writeheader()

        row_index = {r['url']: r for r in reader_old}

        for row in reader_new:
            if row['url'] in row_index:
                if row['hash'] == row_index[row['url']]['hash']:
                    message = 'SAME'
                else:
                    message = 'UPDATED'
            else:
                message = 'NEW'
            row['diff'] = message
            writer.writerow(row)
    logging.info("Created " + diff + " file.")


def main():
    """ Pass in arguments """
    args = get_args()
    new = args.new
    old = args.old
    diff = args.diff
    initialize_logger('add_hash')
    try:
        if check_header(old) and check_header(new):
            identify_diffs(old, new, diff)
    except Exception as ex:
        logging.error(ex)


if __name__ == '__main__':
    main()