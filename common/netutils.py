import requests
import feedparser
from bs4 import BeautifulSoup


def get_pages(*urls):
    '''
    return a list of response objects that were OK
    '''
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            yield response


def get_rss_feed(url):
    '''
    fetch the rss feed from url and parse it
    '''
    return feedparser.parse(url)


def extract_urls_from_rss(feed):
    '''
    returns a list of urls linked to by this feed
    '''
    return [x['href'] for entry in feed.entries for x in entry.links]


def extract_urls_from_html(html):
    '''
    extracts all urls linked to from a given html document
    '''
    soup = BeautifulSoup(html)
    return [x['href'] for x in soup.find_all('a', href=True)]
