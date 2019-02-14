import os
import hashlib
import requests


def get_remote_sha_sum(url):
    """put remote file in memory and create hash"""
    MAXSIZE = 26214400 # 25MB
    response = requests.get(url)

    try:
        response.raise_for_status()
        if len(response.content) < MAXSIZE:
            sha1 = hashlib.sha1()
            response = response.content
            sha1.update(response)
            return sha1.hexdigest()
        else:
            print('Skipping ' +  url + ' because ' + str(MAXSIZE/819200) + 'MB is really big.')
    except requests.exceptions.HTTPError as e:
        return "Error at url %(url)s: %(error)s" % dict(url=url, error=e)
