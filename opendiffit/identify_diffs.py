import csv
import os
import argparse
import logging
import tempfile
from utils import yes_or_no
from utils import initialize_logger
from utils import check_header
import xlsxwriter
import xlrd
import sys


def get_args():
    example_text = '''
    examples:

    python opendiffit/%(identify_diffs)s --old="old-report.csv" --new="new-report.csv" --diff="diff-report.csv"

    python opendiffit/%(identify_diffs)s --old="old-report.csv" --new="new-report.csv" --diff="-"

    python opendiffit/%(identify_diffs)s --config="my-config-file.yml"

    ''' % {'identify_diffs': os.path.basename(__file__)}

    # parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser = configargparse.get_argument_parser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--config', help='your config file')
    parser.add_argument('--old', help='original csv')
    parser.add_argument('--new', help='new csv')
    parser.add_argument('--diff', help='output csv. use "-" add columns to the existing new csv file (keep a backup).')
    return parser.parse_args()


def identify_diffs(old, new, diff):
    """ Identify rows with changed cells """
    with open(old, 'r', encoding='utf-8-sig') as r_csv_old, \
        open(new, 'r', encoding='utf-8-sig') as r_csv_new, \
        open(diff, 'w', encoding='utf-8-sig') as w_csv_diff:
        reader_old = csv.DictReader(r_csv_old)
        reader_new = csv.DictReader(r_csv_new)
        fieldnames = reader_new.fieldnames
        # TODO: Make this DRY and accomidate any existing column headers automatically
        if 'diff' not in reader_new.fieldnames:
            fieldnames = fieldnames + ['diff']
        if 'comply' not in fieldnames:
            fieldnames = fieldnames + ['comply']
        if 'owns' not in fieldnames:
            fieldnames = fieldnames + ['owns']
        if 'notes' not in fieldnames:
            fieldnames = fieldnames + ['notes']
        if 'count' not in fieldnames:
            fieldnames = fieldnames + ['count']
        writer = csv.DictWriter(w_csv_diff, fieldnames=fieldnames)
        writer.writeheader()

        row_index = {r['url']: r for r in reader_old}
        try:
            for row in reader_new:

                if row['url'] in row_index:

                    if row['hash'] == row_index[row['url']]['hash']:
                        row['diff'] = 'SAME'
                        row['comply'] = row_index[row['url']]['comply'] # carry over compliance value from prev report
                        if row_index[row['url']]['notes']:
                            row['notes'] = row_index[row['url']]['notes']
                        if row_index[row['url']]['owns']:
                            row['owns'] = row_index[row['url']]['owns']
                    else:
                        row['diff'] = 'UPDATED'
                        row['comply'] = 'UNKNOWN'
                        if row_index[row['url']]['notes']:
                            row['notes'] = row_index[row['url']]['notes']
                        if row_index[row['url']]['owns']:
                            row['owns'] = row_index[row['url']]['owns']

                else:
                    row['diff'] = 'NEW'
                    row['comply'] = 'UNKNOWN'

                writer.writerow(row)

        except Exception as ex:
            logging.error(ex)
    # logging.info("Created %s file." % (diff))


def main():
    """ Pass in arguments """
    args = get_args()
    new = args.new
    old = args.old
    diff = args.diff
    # output_dir = os.path.dirname(args.new)
    initialize_logger('identify_diffs')


    if check_header(old,['url','hash'],[]) and check_header(new,['url','hash'],[]):
        try:
            identify_diffs(old, new, diff)
            if diff == "-":
                # yes_or_no("Are you sure you want to add the data to the existing '%s' file? (keeping a backup is recommended)" % (input_file))
                os.remove(new)
                os.rename(diff, new)
                logging.info("Updated '%s' file with diff" % (new))
            else:
                logging.info("Created new '%s' file with diff" % (diff))

        except Exception as ex:
            logging.error(ex)


if __name__ == '__main__':
    main()