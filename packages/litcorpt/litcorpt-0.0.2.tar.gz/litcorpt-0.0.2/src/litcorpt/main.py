#!/usr/bin/env python

"""Entry point for Literary corpus in Portuguese"""

import shutil
import os
import tempfile
import datetime
from pathlib import Path

from tinydb import TinyDB

import litcorpt
from litcorpt import settings
from litcorpt.crawlers import gutenberg
from litcorpt.crawlers import dominiopublico


#%%
def retrieve_corpus(verbose=False):
    """This function assures that corpus is available in LITCORPUSPT_DATAPATH.
    If not it will download it.

    TODO:
        (Igor): Return False or raise, if, for some reason, isn't able to
                makes corpus available. Right now is always returning True
    """
    checkin_file = os.path.join(settings.LITCORPUSPT_DATAPATH, 'last.txt')
    if not os.path.exists(checkin_file):

        litcorpuspt_url ="https://github.com/igormorgado/litcorpt_data/archive/refs/heads/main.zip"

        if verbose :
            print(f"Corpus not found in {settings.LITCORPUSPT_DATAPATH}.")

        Path(settings.LITCORPUSPT_DATAPATH).mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Build destination filepath
            filename = 'main.zip'

            if verbose:
                print(f"Downloading from {litcorpuspt_url}")
            # Download corpus
            filepath, _ = litcorpt.utils.download_file(litcorpuspt_url,
                                                       dstdir=tmpdirname,
                                                       filename=filename)

            if verbose:
                print(f"Extracting to {settings.LITCORPUSPT_DATAPATH}")
            # Extract Corpus
            shutil.unpack_archive(filepath, settings.LITCORPUSPT_DATAPATH, "zip")

        # Fill the success timestamp
        with open(checkin_file, 'w') as checkin_fd:
            now = datetime.datetime.now()
            timestamp = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}'
            checkin_fd.write(timestamp)

        if verbose:
            print(f"Completed at {str(now)}.")
    else:
        # Corpus found
        if verbose:
            print(f"Corpus found in {settings.LITCORPUSPT_DATAPATH}.")

    return True

#%%
def load_corpus(rebuild=False, verbose=False):
    """Load corpus. Download if needed. Returns a pandas dataframe
    with corpus or None on fail.

    Inputs:
        rebuild (Bool): Rebuild corpus.db even if it exists. Useful when
                        data is corrupted or was changed directly on file
                        (not so common).

    Outputs:
        corpus (tinyDB): Corpus as pandas dataframe or None
    """

    # Makes sure corpus if available otherwise return None
    if not retrieve_corpus(verbose=verbose):
        return None

    corpusdb_filename = 'corpus.db'
    corpusdb_filepath = os.path.join(settings.LITCORPUSPT_DATAPATH,
                                     corpusdb_filename)

    if not os.path.exists(corpusdb_filepath) or rebuild:
        # zip dirname is: repository-branch
        corpus = {}
        litcorpuspt_dirname = "litcorpt_data-main"

        gutenberg_dir = 'gutenberg_org'
        settings.GUTENBERG_DATAPATH = os.path.join(settings.LITCORPUSPT_DATAPATH,
                                                   litcorpuspt_dirname,
                                                   gutenberg_dir)
        gutenberg_books = gutenberg.load(verbose=verbose)
        corpus.update(gutenberg_books)

        dominiopublico_dir = 'dominiopublico_gov_br'
        settings.DOMINIOPUBLICO_DATAPATH = os.path.join(settings.LITCORPUSPT_DATAPATH,
                                                        litcorpuspt_dirname,
                                                        dominiopublico_dir)
        dominiopublico_books = dominiopublico.load(verbose=verbose)
        corpus.update(dominiopublico_books)

        corpusdb = TinyDB(corpusdb_filepath)

        if verbose:
            print("Building corpus dataset")

        corpusdb.insert_multiple( metadata for _, metadata in corpus.items())
    else:
        if verbose:
            print("Loading corpus dataset")
        corpusdb = TinyDB(corpusdb_filepath)

    return corpusdb

#%%
def corpus(corpusdb, query=None):
    """Return a corpus list from corpusdb and a query (optional)

    Input:
        corpusdb (db): A Corpus database handler
        query (query): A query request. If no query is given, returns the whole corpus.

    Output:
        corpus (list): A list where each element is a document from corpus.
    """
    if query is None:
        search = corpusdb.all()
    else:
        search = corpusdb.search(query)

    corpus = []
    for documents in search:
        for document in documents['contents']:
            corpus.append(document)
    return corpus



#%%
if __name__ == '__main__':
    pass
