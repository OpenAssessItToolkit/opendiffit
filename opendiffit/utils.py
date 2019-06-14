import csv
import os
import logging
import hashlib
import requests
import wget


def initialize_logger(module):
    """ Configure logging """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


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
            logging.info('Skipping ' +  url + ' because ' + str(MAXSIZE/819200) + 'MB is really big.')
    except requests.exceptions.HTTPError as e:
        return "%(error)s:" % dict(error=e)


def check_header(csv_file):
    """ Check if required column headers exist """
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as r_csvfile:
            reader = csv.DictReader(r_csvfile, dialect='excel')

            if ('url' not in reader.fieldnames):
                logging.info("No 'url' header exists in " + csv_file + ". Check headers. Check that file is 'utf-8-sig'.")
                return False
            elif ('hash' not in reader.fieldnames):
                logging.info("No 'hash' header exists in " + csv_file + ". Check headers. Hash is necessary to test if a file with the same name has changed, and needs review.")
                return False
            else:
                return True
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