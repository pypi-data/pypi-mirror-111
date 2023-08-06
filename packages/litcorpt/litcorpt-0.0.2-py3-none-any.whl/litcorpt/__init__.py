"""litcorpt module initialization"""

from tinydb import Query

from litcorpt import settings
from litcorpt.crawlers.gutenberg_crawl import download_all_books as gutenberg_download_all_books
from litcorpt.crawlers.gutenberg_preproc import preprocess as gutenberg_preprocess
from litcorpt.crawlers.dominiopublico import download_all_books as dominiopublico_download_all_books
from .main import load_corpus
from .main import corpus

__version__ = '0.0.2'
__author__ = 'Igor Morgado'
__author_email__ = 'morgado.igor@gmail.com'

settings.init()
