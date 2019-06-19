import csv
import os
import logging
import hashlib
import requests
import wget


def initialize_logger(module, output_dir):
    """ Configure logging """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # create debug file handler and set level to debug
    # handler = logging.FileHandler(os.path.join(output_dir, 'log-' + module + '.log'),'w')
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)


def get_remote_sha_sum(url):
    """ Put remote file in memory and create hash """
    MAXSIZE = 26214400 # 25MB
    response = requests.get(url)
    # TODO only process 200
    try:
        response.raise_for_status()
        if len(response.content) < MAXSIZE:
            sha1 = hashlib.sha1()
            response = response.content
            sha1.update(response)
            return sha1.hexdigest()
        else:
            logging.info('Skipping %s because  %s MB is really big.' % (url, str(MAXSIZE/819200)))
    except requests.exceptions.HTTPError as e:
        return "%(error)s:" % dict(error=e)


def check_header(csv_file, good_headers, bad_headers):
    """ Check if required column headers exist """
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as r_csvfile:
            reader = csv.DictReader(r_csvfile, dialect='excel')

            for bad_header in bad_headers:
                if bad_header in reader.fieldnames:
                    logging.warning("A '%s' column is already here. Check headers in this file and ensure that file is 'utf-8-sig." % (bad_header))
                    raise SystemExit
                else:
                    continue

            for good_header in good_headers:
                if good_header not in reader.fieldnames:
                    print('not')
                    logging.warning("A '%s' column is required to compare files. Check headers this file and ensure that file is 'utf-8-sig." % (good_header))
                    raise SystemExit
                else:
                    return True
    except TypeError as ex:
        logging.warning("Something might be wrong with the headers in this file. %s" % (ex))
    except Exception as ex:
        logging.warning(ex)

def download_changed(url_link):
    try:
        wget.download(url_link)
    except Exception as ex:
        logging.info(url_link)
        logging.info(ex)
        return False

# TODO: add util for testing if PDF is tagged