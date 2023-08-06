#!/usr/bin/env python3

"""Retrieve dominiopublico ebooks"""

import os
import pickle
import time
from urllib.parse import urljoin, urlencode, parse_qs, urlparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup as bs

from litcorpt import settings
from litcorpt import utils

#%%
def retrieve_booklist(category_id=0, verbose=False):
    """ Retrieve a book list for a given category_id in Dominiopublico.gov.br

    Input:
        category_id: int

    Output:
        books (dict): A dicionary with keys as book id and values
        with bookpaths to online metadata and files contents
    """
    assert category_id != 0, "You must supply a category_id"

    query = {
              'first': 3000,
              'co_categoria': 2,
              'select_action': 'Submit',
              'co_midia': 2,
              'co_idioma': 1,
            }

    # Build url to request
    query['co_categoria'] = category_id
    url = f'{settings.DOMINIOPUBLICO_URL}?{urlencode(query)}'

    if verbose:
        print (f"Retrieving booklist from {url}")

    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    booktable_soup = soup.find('table', { 'class': 'displaytagTable' }).tbody

    # Build a list with book names and it's hrefs
    booktable = []
    for tr in booktable_soup.findAll('tr'):
        anchor = tr.findAll('td')[2].find('a')
        if anchor is not None:
            title = anchor.text.strip()
            href = anchor['href']
            booktable.append((title, href))

    # Build books dictionary
    books = {}
    for title, href in booktable:
        qs_dict =  parse_qs(urlparse(href).query)
        bookid = qs_dict.get('co_obra', '[]')[0]
        books[bookid] = {
                'sourcekey': bookid,
                'title': title,
                'href': href}

    return books

#%%
def retrieve_book_metadata(metadata):
    """ Retrieve metadata for given bookid and metadata

    TODO: Handle EDITOR if Author is missing

    Input:
        bookid (str): A bookid
        local_metadata (dict): A dictionary containing a book metadata
                         must contain at least 'href' key filled.


    Output:
        booktable (dict): A book dict with pre-preocessed metadata.

    """
    local_metadata = metadata.copy()
    book_path = local_metadata['href']
    book_url = urljoin(settings.DOMINIOPUBLICO_URL, book_path)
    book_response = requests.get(book_url)
    # Raise if rerquest fails
    book_response.raise_for_status()
    book_soup = bs(book_response.text, 'html.parser')

    table = book_soup.find('td', {'class': 'detalhe1'}).find_parent('table')

    #%% Build book dictionary entry
    booktable = {}
    for tr in table.findAll('tr'):
        header, _, content = tr.findAll('td')
        header = header.text.strip()

        header_map = { 'Título:': 'title',
                       'Autor:': 'authors',
                       'Categoria:': 'category',
                       'Idioma:': 'language',
                       'Instituição:/Parceiro': 'datasource',
                       'Ano da Tese': 'year',
                       'Acessos:': 'hits', }

        headers_to_ignore = [ 'hits' ]

        header = header_map.get(header, '')

        if content.a is not None and header == '':
            header = 'filehref'
            content = content.a['href']
        else:
            content = content.text.strip()

        if header == '' or content == '':
            continue

        if header not in headers_to_ignore:
            booktable[header] = content

    #%% Convert Authors into a list and split name/surname
    author_list = booktable['authors'].split(' ')
    booktable['authors'] = [{ 'lastname': author_list[-1],
                             'firstname': ' '.join(author_list[0:-1]),
                             'life': ''
                           }]

    # Convert to list
    booktable['category'] = [ booktable['category'] ]
    booktable['language'] = [ booktable['language'] ]

    local_metadata.update(booktable)
    return local_metadata

#%%
def retrieve_metadata(books, max_retries=5, verbose=False):
    """ Retrieve "all"  metadata, from a  book list.


    Input:
        books (dict): A dict with books. key is the book id, val is a dict of metadata. The metadata
                      must contain at least 'href' key, pointing to gutenberg.org ebook page.

    Returns:
        books (dict): The books dictionary filled with existent metadata
    """
    failed_ids = []
    for bookid, metadata in books.items():
        if verbose:
            print(f"{bookid}: Retrieving metadata")
        request_failure = True
        for count in range(max_retries):
            try:
                books[bookid] = retrieve_book_metadata(metadata)
            except requests.HTTPError:
                print(f"{bookid}: Metadata not found.")
                break
            except requests.ConnectionError:
                # Maybe server asking for a slowdown
                print(f"{bookid}: Lets slow down for 60 seconds ({count+1}/{max_retries})")
                time.sleep(60)
            else:
                request_failure = False
                break

        if request_failure:
            failed_ids.append(bookid)

    # Cleanup failed retrivals
    for failed_id in failed_ids:
        del books[failed_id]

    return books

#%%
def retrieve_book(book_entry):
    """Retrieve a book from a book dict entry and store on DOMINIOPUBLICO_DATAPATH"""
    bookfile_url = urljoin(settings.DOMINIOPUBLICO_URL, book_entry['filehref'])
    filepath, filesize = utils.download_file(bookfile_url,
                                             dstdir=settings.DOMINIOPUBLICO_DATAPATH,
                                             verbose=True)
    return filepath, filesize

#%%
def dump_info(filepath, metadata):
    """Write metadata info to filepath"""
    with open(filepath, 'w') as book_info_fd:
        info_values = []
        info_values.append(metadata['sourcekey'])
        info_values.append(metadata.get('title', ''))
        authors = metadata.get('authors', [{}])
        author = authors[0]
        info_values.append(author.get('lastname', ''))
        info_values.append(author.get('firstname', ''))
        editors = metadata.get('editors', [{}])
        editor = editors[0]
        info_values.append(editor.get('lastname', ''))
        info_values.append(editor.get('firstname', ''))
        info_values.append(';'.join(metadata.get('language', [])))
        info_values.append(';'.join(metadata.get('subject', [])))
        info_values.append(';'.join(metadata.get('category', [])))
        info_values_str = ','.join(info_values)
        info_values_str += '\n'
        book_info_fd.write(info_values_str)

#%%
def dump_pickle(filepath, book_entry):
    """Write book_entry dict to filepath"""
    with open(filepath, 'wb') as book_pickle_fd:
        meta = book_entry.copy()
        pickle.dump(meta, book_pickle_fd)

#%%
def dump_metadata(book_entry, filepath, verbose=False):
    """Write book metadata  in DOMINIOPUBLICO_DATAPATH"""
    dirname = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, _ = os.path.splitext(filename)
    info_filename = f"{name}-info.txt"
    pickle_filename = f"{name}.p"

    info_filepath = os.path.join(dirname, info_filename)
    pickle_filepath = os.path.join(dirname, pickle_filename)

    if verbose:
        print(f"{book_entry['sourcekey']}: Dump info to {info_filepath}")
    dump_info(info_filepath, book_entry)

    if verbose:
        print(f"{book_entry['sourcekey']}: Dump pickle to {pickle_filepath}")
    dump_pickle(pickle_filepath, book_entry)

#%%
def retrieve_books(books, max_retries=5, verbose=False):
    """Retrieve all books from a book dict and save them on DOMINIOPUBLICO_DATAPATH"""
    failed_ids = []
    for bookid, metadata in books.items():

        if verbose:
            print(f"{bookid}: Retrieving file {metadata['filehref']}")

        request_failure = True
        for count in range(max_retries):
            # By default we have a failure
            filesize = 0
            try:
                filepath, filesize = retrieve_book(metadata)
            except requests.HTTPError:
                print(f"{bookid}: Book not found.")
                break
            except requests.ConnectionError:
                # Maybe server asking for a slowdown
                print(f"{bookid}: Lets slow down for 60 seconds ({count+1}/{max_retries})")
                time.sleep(60)
            else:
                dump_metadata(metadata, filepath, verbose=verbose)
                request_failure = False
                break


        if (filesize == 0) or request_failure:
            failed_ids.append(bookid)

    return failed_ids

#%%
def load_book(bookid, book_path):
    """ Load book given bookpaths

    TODO: Handle if files are missing. Right now it will break.

    Input:
        bookid (str):  A book id
        bookpath (str): A path to book data

    Output:
        book (dict): A book entry
    """

    book_pickle_filename = f'{bookid}.p'
    book_pickle_filepath = os.path.join(book_path, book_pickle_filename)

    book_content_filename = f'{bookid}.txt'
    book_content_filepath = os.path.join(book_path, book_content_filename)


    # Build bookmeta dict with empty contents
    try:
        with open(book_pickle_filepath, 'rb') as book_pickle_fd:
            bookmeta = pickle.load(book_pickle_fd)
            bookmeta['contents'] = []
    except FileNotFoundError:
        return None

    # Read file contents (only a single file right now)
    try:
        with open(book_content_filepath, 'rb') as book_content_fd:
            contents = book_content_fd.read()
            contents = str(contents, 'utf-8')
            bookmeta['contents'].append(contents)
    except FileNotFoundError:
        return None

    return bookmeta

#%%
def load(verbose=False):
    """Load all DominioPublico books from DOMINIOPUBLICO_DATAPATH

    Outputs: (dict) A dicionary with all dominio publico books"""

    bookdirs = [x
                for x in os.listdir(settings.DOMINIOPUBLICO_DATAPATH)
                if os.path.isdir(os.path.join(settings.DOMINIOPUBLICO_DATAPATH, x))]

    books = {}
    for bookdir in bookdirs:
        bookid = bookdir
        if verbose:
            print(f"{bookid}\t", end="")
        bookpath = os.path.join(settings.DOMINIOPUBLICO_DATAPATH, bookdir)
        bookmeta = load_book(bookid, bookpath)
        if bookmeta is not None:
            books[bookid] = bookmeta

    print()
    return books



def pick_problems(data):
    """Return a sub dictionary containing only entries that triggered an issue (for testing)"""
    problems = [ '2129', '86692', '184139', '1806' ]

    samples = { key: meta for key, meta in data.items() if key in problems }

    return samples

#%%
def download_all_books(testmode=False, verbose=False):
    """This function mirrors portuguese books from dominiopublico.gov.br

    Outputs:
        books_sz: Number of books downloaded
    """

    settings.DOMINIOPUBLICO_DATAPATH = os.environ.get('DOMINIOPUBLICO_DATAPATH',
                                                      '~/data/dominiopublico')
    settings.DOMINIOPUBLICO_DATAPATH = os.path.expanduser(settings.DOMINIOPUBLICO_DATAPATH)
    Path(settings.DOMINIOPUBLICO_DATAPATH).mkdir(parents=True, exist_ok=True)

    categories = { 2: 'literatura',
                   20: 'artes',
                   33: 'literatura infantil',
                   54: 'filosofia',
                 }

    books = {}
    for category_id in categories:
        books_cat = retrieve_booklist(category_id, verbose=verbose)
        books.update(books_cat)

    if testmode:
        books = pick_problems(books)
        #books = utils.dict_random_samples(books, 5)

    books = retrieve_metadata(books, verbose=verbose)
    failed_ids = retrieve_books(books, verbose=verbose)
    for failed_id in failed_ids:
        del books[failed_id]

    return books
