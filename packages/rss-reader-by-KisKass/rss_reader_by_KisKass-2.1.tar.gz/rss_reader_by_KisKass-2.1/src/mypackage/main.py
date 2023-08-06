import urllib.request
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import json
import logging

parser = argparse.ArgumentParser()

parser.add_argument('source', help='Set rss url')
parser.add_argument('--version',
                    action='version', version='version 2.0',
                    help='Print version info')
parser.add_argument('--json',
                    action="store_true",
                    help='Print result as JSON in stdout')
parser.add_argument('--verbose',
                    action="store_true",
                    help='Outputs verbose status messages')
parser.add_argument('--limit',
                    type=int,
                    default=0,
                    help='Limit news topics if this parameter provided')
args = parser.parse_args()


def output_json(verbose=False):
    """json style output"""
    soup = parse_url(args.source, verbose)
    data_set = {'Feed': soup.source.string}
    news = parse_news(soup, args.limit, verbose)
    i = 0
    for n in news:
        data_set['item' + str(i)] = {'Title': n.title.text,
                                     'Date': n.pubDate.string,
                                     'Link': n.link.string}
        i += 1
    json_dump = json.dumps(data_set, indent=4, ensure_ascii=False)
    print(json_dump)


def parse_url(source: str, verbose):
    """Gets xml from url.

        Keyword arguments:\n
        source -- url of rss feed\n
        verbose -- checking presence verbose argument(default=False)

        Return:\n
        soup -- a BeautifulSoup object, which represents the document as a nested data structure"""

    with urllib.request.urlopen(source) as f:
        logging.info(f"{datetime.now()}: Successful connecting {source}")
        if verbose:
            print(logging.info(f"{datetime.now()}: Successful connecting {source}"))
        soup = BeautifulSoup(f, "xml")
        logging.info(f"{datetime.now()}: Successful xml parsing {source}")
        if verbose:
            print(logging.info(f"{datetime.now()}: Successful xml parsing {source}"))
    return soup


def parse_news(soup, limit_=0, verbose=False):
    """Gets items from xml

    soup - a BeautifulSoup object

    limit - number of news to return
    \nverbose -- checking presence verbose argument(default=False)
    """
    # ic('Parsing news')
    if limit_:
        soup_news =  soup.find_all('item', limit=limit_)

    else:
        soup_news = soup.find_all('item')
    logging.info(f"{datetime.datetime.now()}: Successful news parsing from xml")
    if verbose:
        print(logging.info(f"{datetime.datetime.now()}: Successful news parsing from xml"))
    return soup_news


def normal_output():
    """Normal output"""
    soup = parse_url(args.source)
    print(soup.title.text)
    news = parse_news(soup, args.limit)
    for n in news:
        print(f'Title: {n.title.text}')
        print(f'Date: {n.pubDate.string}')
        print(f'Link: {n.link.string}\n')
        # ниже код который выводит подробности новости но т.к. он замедляет работу программы я его временно убрал
        # with urllib.request.urlopen(n.link.string) as f:
        #    item_details = BeautifulSoup (f, "lxml",)
        #    for item_detail in item_details.find_all('p'):
        #        if item_detail.text != '':
        #            print(item_detail.text)
        #            break
        #    print('-----------')
        pass


def main():
    logging.basicConfig(filename='logfile.log', level=logging.INFO)


    if args.verbose:
        verbose = True

    try:
        if args.json:
           output_json(verbose)
        else:
           normal_output(verbose)
    except Exception as ex:
        logging.error(f"{datetime.now()}: {ex}")
        if verbose:
            print(logging.error(f"{datetime.now()}: {ex}"))
