from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.pdfdevice import TagExtractor
from pdfminer3.pdfpage import PDFPage
from io import BytesIO

from utils import initialize_logger
from utils import check_header

import tempfile
import csv
import argparse
import logging
import requests
import wget
import os


from urllib.parse import unquote

dir_path = os.path.dirname(os.path.realpath(__file__))


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

                clean_url = unquote(row['url'])

                if clean_url.endswith('.pdf'):

                    logging.info("Document is a PDF.")

                    if row['diff'] != 'SAME' and row['diff'] != 'SKIP' and row['comply'] != 'YES':

                        logging.info("Document is not the SAME. Try to detect tags.")
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
                            # Get the file name
                            file_name = clean_url.rsplit('/', 1)[-1]
                            temp_download_file_location = tempfile.gettempdir() + '/' + file_name

                            print(temp_download_file_location)
                            if os.path.exists(temp_download_file_location):
                                # Download the file
                                logging.info("File exist already. Use me.")

                            else:
                                the_file_data = wget.download(clean_url, temp_download_file_location)
                                logging.info("File does not exist. Download...")


                            fp = open(temp_download_file_location, 'rb')
                            interpreter = PDFPageInterpreter(rsrcmgr, device)
                            maxpages = 2
                            password = ''
                            caching = True
                            pagenos=set()
                            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
                                interpreter.process_page(page)

                            contents = retstr.getvalue().decode()
                            print(contents)
                            fp.close()
                            device.close()
                            retstr.close()

                            # check if common proprietary Acrobat tags are in the response
                            tags = ["<b\'Heading 1\'", "<b\'Heading 2\'", "<b\'Part\'", "<b\'Sect\'", "<b\'Art\'", "<b\'Content\'", "<b\'Index\'", "<b\'BibEntry'", "<b\'Lbl\'", "<b\'Index\'", "<b\'Note\'", "<b\'Reference\'", "<b\'Span\'", "<b\'P\'", "<b\'Figure\'", "<b\'Artifact\'", "<b\'ArtifactSpan\'", "<b\'LBody\'", "<b\'Normal\'", "\'Annots\'"]
                            for tag in tags:
                                logging.info("Found tag %s" % (tag))
                                if "<b\'Heading 1\'" in contents or "<b\'Heading 2\'" in contents:
                                    logging.info("Found tag %s" % (tag))
                                    row['comply'] = 'MAYBE'
                                    row['notes'] = ' Is Tagged. Has a Heading Tag.'
                                    break
                                elif tag in contents:
                                    logging.info("Found tag %s" % (tag))
                                    row['comply'] = 'MAYBE'
                                    row['notes'] = ' Is Tagged. But needs a Heading Tag'
                                    break
                                else:
                                    row['comply'] = 'NO'
                                    row['notes'] = 'Not Tagged.'

                        except Exception as ex:
                            logging.error(ex)
                    else:
                       logging.info("Document is the 'SAME'. Skip it.")

                else:
                    logging.info("Document is not PDF. Skip it.")

                writer.writerow(row)
        except Exception as ex:
            logging.error(ex)


def main():
    """ Pass in arguments """
    args = get_args()
    input_file = args.input_file
    output_file = args.output_file
    output_dir = os.path.dirname(args.input_file)
    initialize_logger('detect_tags', output_dir)

    if check_header(input_file,['url','comply','diff'],[]):

        try:
            detect_tags(input_file,output_file)
            if output_file == "-":
                # yes_or_no("Are you sure you want to add the data to the existing '%s' file? (keeping a backup is recommended)" % (input_file))
                os.remove(input_file)
                os.rename(output_file, input_file)
                logging.info("Updated '%s' 'comply' column " % (input_file))
            else:
                logging.info("Created new '%s' file with updated 'comply' column" % (output_file))

        except Exception as ex:
            logging.error(ex)


if __name__ == '__main__':
    main()
