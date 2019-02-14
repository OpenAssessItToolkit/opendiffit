import csv
import os
import argparse
from remote_sha import get_remote_sha_sum


def get_args():
    example_text = '''
    examples:

    python opendiffit/%(add_hash)s --input-file="report.csv"

    ''' % {'add_hash': os.path.basename(__file__)}

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input-file', help='original csv')
    return parser.parse_args()


def add_hash(input_file):
    """Add new column with hash"""
    output_file = input_file + '_hashed.csv'
    with open(input_file, 'r', encoding='utf-8-sig') as r_csvfile, open(output_file, 'w', encoding='utf-8-sig') as w_csvfile:
        reader = csv.DictReader(r_csvfile)
        fieldnames = reader.fieldnames + ['hash']
        writer = csv.DictWriter(w_csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row['hash'] = get_remote_sha_sum(row['url'])
            writer.writerow(row)
            print('Hashed')


def check_header(input_file):
    """Check if required column headers exist"""
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        if 'url' in reader.fieldnames:
            return True
        else:
            print("This csv is invalid or has no 'url'.")
            return False


def main():
    """Pass arguments, check csv validity, and add hash"""
    args = get_args()
    input_file = args.input_file

    if check_header(input_file):
        add_hash(input_file)
    else:
        print("Check contents of csv.")

    print('Done adding hashes.')

if __name__ == '__main__':
    main()