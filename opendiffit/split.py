import csv
import os
import argparse
import logging
import re
from urllib.parse import urlparse
from utils import initialize_logger
from utils import check_header


def get_args():
    example_text = '''
    examples:

    python opendiffit/%(split)s --input-file="report.csv"

    ''' % {'split': os.path.basename(__file__)}

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input-file', help='original csv')
    parser.add_argument('-o', '--output-dir', help='directory to output the new csv files')
    return parser.parse_args()


def split(input_file,output_dir):
    """ Split csv by vhost column """
    with open(input_file, 'r', encoding='utf-8-sig') as r_csvfile:
        reader = csv.DictReader(r_csvfile)
        # Category -> open file lookup
        outputs = {}
        for row in reader:
            url = row['url']
            parsed_uri = urlparse(url)
            domain = '{uri.netloc}'.format(uri=parsed_uri)

            # Open a new file and write the header
            if domain not in outputs:
                location = output_dir + '{}_only.csv'.format(re.sub('[^A-Za-z0-9]+', '', domain))
                w_csvfile = open(location, 'w', encoding='utf-8-sig')
                writer = csv.DictWriter(w_csvfile, fieldnames=reader.fieldnames)
                writer.writeheader()
                outputs[domain] = w_csvfile, writer
                logging.info("Saved split csv files into " + location)
            # Always write the row
            outputs[domain][1].writerow(row)

        # Close all the files
        for w_csvfile, _ in outputs.values():
            w_csvfile.close()



def main():
    """ Pass arguments, check csv validity, and add hash """
    args = get_args()
    input_file = args.input_file
    output_dir = args.output_dir
    initialize_logger('add_hash')
    try:
        if check_header(input_file,):
            split(input_file,output_dir)
    except Exception as ex:
        logging.error(ex)

if __name__ == '__main__':
    main()