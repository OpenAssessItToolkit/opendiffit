from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.pdfdevice import TagExtractor
from pdfminer3.pdfpage import PDFPage
from io import BytesIO

from utils import initialize_logger
from utils import check_header

import csv
import argparse
import logging
import requests
import wget
import os


def get_args():
    example_text = '''
    examples:

    python opendiffit/%(detect_tags)s --input-file="input.csv" --output-file="input_with_comply.csv"

    ''' % {'detect_tags': os.path.basename(__file__)}

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input-file', help='original csv')
    parser.add_argument('-o', '--output-file', help='comply version of csv. Use "-" overwrite the current file (keep a backup).')
    return parser.parse_args()


def detect_tags(input_file, output_file):
    """ Identify PDFs that are tagged """
    with open(input_file, 'r', encoding='utf-8-sig') as r_csvfile, \
        open(output_file, 'w', encoding='utf-8-sig') as w_csvfile:
        reader = csv.DictReader(r_csvfile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(w_csvfile, fieldnames=fieldnames)
        writer.writeheader()

        try:
            for row in reader:

                # if row['diff'] != 'SAME' and row['url'].lower().endswith('.pdf'):
                if row['diff'] != 'SAME':

                    logging.info("It is not the SAME. Try to detect tags.")

                    rsrcmgr = PDFResourceManager()
                    retstr = BytesIO()

                    try:
                        try:
                            device = TagExtractor(rsrcmgr, retstr, codec='utf-8')
                        except:
                            logging.info('Not utf-8.')
                        try:
                            device = TagExtractor(rsrcmgr, retstr, codec='ascii')
                        except:
                            logging.info('Not ascii.')
                    except Exception as ex:
                        logging.error(ex)

                    try:
                        # Download the file
                        the_file_data = wget.download(row['url'])

                        # Get the file name
                        the_file_name = row['url'].rsplit('/', 1)[-1]


                        fp = open(the_file_name, 'rb')
                        interpreter = PDFPageInterpreter(rsrcmgr, device)
                        maxpages = 1
                        password = ''
                        caching = True
                        pagenos=set()
                        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
                            interpreter.process_page(page)

                        contents = retstr.getvalue().decode()

                        fp.close()
                        device.close()
                        retstr.close()

                        # check if common proprietary Acrobat tags are in the response
                        tags = ["<b\'Part\'", "</b\'Sect\'", "</b\'Art\'", "<b'Content'", "<b\'Artifact\'"]
                        for tag in tags:
                            if tag not in contents:
                                row['comply'] = 'NO'
                                # return False
                            else:
                                logging.info("Found tag %s" % (tag))
                                row['comply'] = 'MAYBE'
                                break
                                # return True

                    except Exception as ex:
                        logging.error(ex)

                else:
                    logging.info("It is the SAME. Skip it.")

                writer.writerow(row)
        except Exception as ex:
            logging.error(ex)

    # os.remove(the_file_name)

def main():
    """ Pass in arguments """
    args = get_args()
    input_file = args.input_file
    output_file = args.output_file
    output_dir = os.path.dirname(args.input_file)
    initialize_logger('detect_tags', output_dir)

    if check_header(input_file,['url','comply'],[]):

        try:
            if output_file == "-":
                # yes_or_no("Are you sure you want to add the data to the existing '%s' file? (keeping a backup is recommended)" % (input_file))
                os.remove(input_file)
                os.rename(output_file, input_file)
                logging.info("Updated '%s' comply column " % (input_file))
            else:
                logging.info("Created new '%s' file with updated comply column" % (output_file))
            detect_tags(input_file,output_file)

        except Exception as ex:
            logging.error(ex)


if __name__ == '__main__':
    main()
