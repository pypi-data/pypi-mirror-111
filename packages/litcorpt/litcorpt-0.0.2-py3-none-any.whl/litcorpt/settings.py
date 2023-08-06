import os

def init():
    global GUTENBERG_URL
    GUTENBERG_URL = "http://www.gutenberg.org/browse/languages/pt"

    global GUTENBERG_DATAPATH
    GUTENBERG_DATAPATH = ""

    global DOMINIOPUBLICO_URL
    DOMINIOPUBLICO_URL = "http://www.dominiopublico.gov.br/pesquisa/ResultadoPesquisaObraForm.do"

    global DOMINIOPUBLICO_DATAPATH
    DOMINIOPUBLICO_DATAPATH = ""

    global LITCORPUSPT_DATAPATH
    LITCORPUSPT_DATAPATH = os.environ.get('LITCORPUSPT_DATAPATH', '~/litcorpt_data')
    LITCORPUSPT_DATAPATH = os.path.expanduser(LITCORPUSPT_DATAPATH)

if __name__ == '__main__':
    pass
