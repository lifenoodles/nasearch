from django.core.management.base import BaseCommand, CommandError
from shownotes.models import Show, Entry
from bs4 import BeautifulSoup
import feedparser
import requests


def get_pages(links):
    for link in links:
        response = requests.get(link)
        if response.status_code == 200:
            yield response


def get_feed(name):
    return feedparser.parse(name)


def extract_links_from_entry(entry):
    return [x['href'] for x in entry.links]


def extract_links_from_html(html):
    soup = BeautifulSoup(html)
    return [x['href'] for x in soup.find_all('a', href=True)]


def show_exists(show_id):
    return False


class Command(BaseCommand):
    NA_RSS_URL = 'http://feed.nashownotes.com/'
    help = 'Fetches updates from the no agenda rss feed'

    def handle(self, *arks, **options):
        feed = get_feed(Command.NA_RSS_URL)

        shownote_links = map(extract_links_from_entry, feed.entries)
        shownote_links = [entry for sublist in shownote_links
                          for entry in sublist
                          if 'noagendanotes' in entry]

        # DEBUG, just run for 1 show
        shownote_links = [shownote_links[0]]

        # visit opml for each link pointed to
        opmls = []
        for response in get_pages(shownote_links):
            opmls += filter(lambda x: '.opml' in x,
                            extract_links_from_html(response.text))

        for opml in get_pages(opmls):
            pass

        self.stdout.write(repr(opmls))

        # check if these show notes exist in the database

        # if it doesn't
            # insert
        # if it's newer
            # update
