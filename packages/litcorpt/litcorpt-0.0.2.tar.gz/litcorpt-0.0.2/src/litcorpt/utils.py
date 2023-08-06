"""This module contains utilities for litcorpt API"""

import os
import random
import re
from urllib.parse import urlparse

import requests

def dict_slice(contents, n):
    """Helper function to retrieve the first n elements in a dictionary"""
    return dict(list(contents.items())[:n])

def dict_random_samples(data, n):
    """Return a dictionary with n random entries from data"""
    keylist = list(data.keys())
    random.shuffle(keylist)
    samples = {}
    for key in keylist[:n]:
        samples[key] = data[key]

    return samples

def download_file(url, dstdir='.', filename=None, verbose=False):
    """Download file from url and save as dstdir/filepath. If filename is omitted
       check if http requests gives a filename, otherwise use url path
       filename and save at dstdir. This do not create the
       dir structure, that must be created beforehand.

    Input:
        url (str): Url to download
        filename (str): Filename to download to. If missing try to figure out.
        dstdir (str): Directory to store data
        verbose (bool): Be verbose or not

    Outputs:
        local_filepath (str): Filepath to downloaded file
        filesize (int): Ammount of bytes downloaded

    TODO:
        (Igor): Add a download bar if verbose is true.
    """

    local_filename = ""
    local_url = url
    with requests.get(url, stream=True) as req:
        req.raise_for_status()

        # Check if filepath was given, otherwise find from request
        if filename:
            # Name was given
            local_filename = filename
        else:
            # Name from http headers
            if 'content-disposition' in req.headers:
                disposition = req.headers['content-disposition']
                local_filename = re.findall("local_filepath=(.+)", disposition)[0]

            # We got a redirect
            if len(req.history) > 0:
                hist_req = req.history[0]
                if hist_req.status_code == 302:
                    local_url = hist_req.headers.get('Location', url)

            # Name from url path
            if len(local_filename) == 0:
                local_filename = urlparse(local_url).path.split('/')[-1]

        # Check filesize (only works when stream=False)
        expected_filesize = 0
        if 'Content-Length' in req.headers:
            expected_filesize = int(req.headers['Content-Length'])

        local_filepath = os.path.join(dstdir, local_filename)
        if verbose:
            print (f'Downloading {url} to {local_filepath}', end='')
            if expected_filesize > 0:
                print(f' with {expected_filesize} bytes', end='')
            print()

        filesize = 0
        with open(local_filepath, 'wb') as f:
            for chunk in req.iter_content(chunk_size=None):
                if chunk:
                    filesize += len(chunk)
                    f.write(chunk)

    return local_filepath, filesize
