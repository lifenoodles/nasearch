from shownotes.models import ShowSource
import requests
import feedparser
from BeautifulSoup import BeautifulSoup
import re


def get_html(url):
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        return response.text
    raise IOError('No text received')


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


def get_links_to(pattern, html):
    '''
    return a list of links that match the given pattern
    '''
    soup = BeautifulSoup(html)
    links = [x['href'] for x in soup.findAll(
        '', {'href': re.compile(pattern)})]
    return list(set(links))


def extract_urls_from_html(html):
    '''
    extracts all urls linked to from a given html document
    '''
    soup = BeautifulSoup(html)
    return [x['href'] for x in soup.find_all('a', href=True)]


def insert_show_source(url, number):
    opml_pattern = '^http://.*\.opml'
    opml_re = re.compile(opml_pattern)

    if not opml_re.match(url):
        text = get_html(url)
        opml_urls = get_links_to(opml_pattern, text)
        assert len(opml_urls) <= 1
        if len(opml_urls) == 0:
            ShowSource(show_number=number, filetype=ShowSource.HTML,
                       text=text).save()
            return True
        else:
            url = opml_urls[0]
    if opml_re.match(url):
        text = get_html(url)
        ShowSource(show_number=number, filetype=ShowSource.OPML,
                   text=text).save()
        return True
    return False
