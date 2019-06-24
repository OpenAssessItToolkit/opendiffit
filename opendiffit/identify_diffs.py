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

    python opendiffit/%(identify_diffs)s --old="old-report.csv" --new="new-report.csv" --diff="-"

    ''' % {'identify_diffs': os.path.basename(__file__)}

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-o', '--old', help='original csv')
    parser.add_argument('-n', '--new', help='new csv')
    parser.add_argument('-d', '--diff', help='output csv. use "-" to default the output file name to input-file__diff.csv')
    return parser.parse_args()

def identify_diffs(old, new, diff):
    """ Identify rows with changed cells """
    with open(old, 'r', encoding='utf-8-sig') as r_csv_old, \
        open(new, 'r', encoding='utf-8-sig') as r_csv_new, \
        open(diff, 'w', encoding='utf-8-sig') as w_csv_diff:
        reader_old = csv.DictReader(r_csv_old)
        reader_new = csv.DictReader(r_csv_new)
        fieldnames = reader_new.fieldnames
        if 'diff' not in reader_new.fieldnames:
            fieldnames = reader_new.fieldnames + ['diff']
        if 'comply' not in reader_new.fieldnames:
            fieldnames = reader_new.fieldnames + ['comply']

        writer = csv.DictWriter(w_csv_diff, fieldnames=fieldnames)
        writer.writeheader()

        row_index = {r['url']: r for r in reader_old}

        for row in reader_new:
            if row['url'] in row_index:
                if row['hash'] == row_index[row['url']]['hash']:
                    row['diff'] = 'SAME'
                    row['comply'] = row_index[row['url']]['comply'] # carry over compliance value from prev report
                else:
                    row['diff'] = 'UPDATED'
                    row['comply'] = 'UNKNOWN'
            else:
                row['diff'] = 'NEW'
                row['comply'] = 'UNKNOWN'
            writer.writerow(row)
    logging.info("Created %s file." % (diff))


def main():
    """ Pass in arguments """
    args = get_args()
    new = args.new
    old = args.old
    diff = args.diff
    output_dir = os.path.dirname(args.new)
    if diff == "-":
        diff = new.replace('.csv','') + '__diff.csv'
    initialize_logger('identify_diffs', output_dir)
    try:
        if check_header(old,['url','hash'],['diff']) and check_header(new,['url','hash'],['diff']):
            identify_diffs(old, new, diff)
    except Exception as ex:
        logging.error(ex)


if __name__ == '__main__':
    main()