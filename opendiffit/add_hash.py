import csv
import os
import argparse
import logging
from utils import initialize_logger
from utils import get_remote_sha_sum
from utils import check_header


def get_args():
    example_text = '''
    examples:

    python opendiffit/%(add_hash)s --input-file="report.csv"

    ''' % {'add_hash': os.path.basename(__file__)}

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input-file', help='original csv')
    parser.add_argument('-o', '--output-file', help='hashed version of csv. use "-" to default the output file name to input-file__hashed.csv')
    return parser.parse_args()


def add_hash(input_file,output_file):
    """ Add new column with hash """
    with open(input_file, 'r', encoding='utf-8-sig') as r_csvfile, \
        open(output_file, 'w', encoding='utf-8-sig') as w_csvfile:
        reader = csv.DictReader(r_csvfile)
        fieldnames = reader.fieldnames + ['hash']
        writer = csv.DictWriter(w_csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                row['hash'] = get_remote_sha_sum(row['url'])
                writer.writerow(row)
                logging.info("Hashing...")
            except Exception as ex:
                logging.error(ex)
    logging.info("Hashing complete.")

def main():
    """ Pass arguments, check csv validity, and add hash """
    args = get_args()
    input_file = args.input_file
    output_file = args.output_file
    if output_file == "-":
        output_file = input_file.replace('.csv','') + '__hashed.csv'
    initialize_logger('add_hash')
    try:
        if check_header(input_file,):
            add_hash(input_file,output_file)
    except Exception as ex:
        logging.error(ex)

if __name__ == '__main__':
    main()