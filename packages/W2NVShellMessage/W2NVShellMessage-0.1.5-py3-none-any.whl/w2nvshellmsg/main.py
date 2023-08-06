import os
import pickle
import pathlib
import concurrent.futures
from dataclasses import dataclass
from random import randrange
import requests
from bs4 import BeautifulSoup
from loguru import logger
from colorama import init as colorama_init, deinit, Fore, Style
colorama_init()

BASE_URL = 'https://nightvale.fandom.com{pg_suff}'
TRANSCRIPT_URL = 'https://nightvale.fandom.com/wiki/Category:Year_{year}_transcripts'
# HERE = pathlib.Path(__file__).parent
# PROJ_ROOT = os.sep.join(str(HERE).split(os.sep)[:-1])
CACHE_DIR = os.path.join(os.path.expanduser('~'), '.cache', 'w2nv')


@dataclass
class Quote:
    text: str
    year: str
    episode: str


def create_cache_dir():
    try:
        os.mkdir(CACHE_DIR)
    except FileExistsError as _e:
        pass


def init():
    create_cache_dir()
    assert chk_url_up(url=BASE_URL.format(pg_suff='')) == True
    lst = fetch()
    save_cache(lst)


def chk_url_up(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    return False


def get_quotes(args):
    href, _ctr = args[0], args[1]
    pg_url = BASE_URL.format(pg_suff=href)
    logger.debug(pg_url)
    response = requests.get(pg_url)
    logger.debug(response.status_code)

    pg_soup = BeautifulSoup(response.text, 'html.parser')
    quote_lst = []
    for p in pg_soup.select('div.mw-parser-output p'):
        quote = Quote(
            text=p.get_text(),
            year=f'Year {_ctr}',
            episode=pg_soup.select(
                'div.mw-parser-output div b')[0].get_text().replace(
                    ' (episode)', ''
            )
        )
        # print(Fore.RED + Style.BRIGHT + quote.text)
        # print(Fore.GREEN + Style.BRIGHT + quote.text)
        # print(Fore.YELLOW + Style.BRIGHT + quote.text)
        # print(Fore.BLUE + Style.BRIGHT + quote.text)
        # print(Fore.MAGENTA + Style.BRIGHT + quote.text)
        # print(Fore.CYAN + Style.BRIGHT + quote.text)
        # print(Fore.WHITE + Style.BRIGHT + quote.text)
        quote_lst.append(quote)
    return quote_lst


def fetch():
    quotes_lst = []
    _ctr = 1
    while True:
        url = TRANSCRIPT_URL.format(year=_ctr)
        logger.debug(url)
        response = requests.get(url)
        logger.debug(response.status_code)
        if response.status_code > 299:
            break
        soup = BeautifulSoup(response.text, 'html.parser')

        a_lst = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if not href or 'wiki/Transcript:' not in href:
                continue
            a_lst.append((href, _ctr,))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(get_quotes, a_lst)
        # for href in a_lst:
        #     quote = get_quotes(href=href)

        for quote_lst_r in results:
            quotes_lst += quote_lst_r

        _ctr += 1
        break

    return quotes_lst


def save_cache(lst):
    with open(os.path.join(CACHE_DIR, 'data.pkl'), 'wb') as lst_p:
        pickle.dump(lst, lst_p)


def show_msg(return_msg=False):
    lst = None
    try:
        with open(os.path.join(CACHE_DIR, 'data.pkl'), 'rb') as lst_p:
            lst = pickle.loads(lst_p.read())
    except FileNotFoundError:
        print('Unable to load cache. Try running w2nv-init.')
        return
    msg = lst[randrange(len(lst))]
    print(
        Fore.CYAN + Style.BRIGHT + f'"{msg.text.strip()}"'
        + Fore.YELLOW + f'\n\t\t\t\t- {msg.year}, {msg.episode}'
    )
    if return_msg:
        return msg


def main():
    show_msg()


if __name__ == '__main__':
    main()


deinit()
