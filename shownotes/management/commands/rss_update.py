from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from shownotes.management.datasources import OpmlLoader
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
    help = 'Fetches updates from the no agenda rss feed'
    NA_RSS_URL = 'http://feed.nashownotes.com/'

    def handle(self, *arks, **options):
        feed = get_feed(Command.NA_RSS_URL)

        shownote_links = map(extract_links_from_entry, feed.entries)
        shownote_links = [entry for sublist in shownote_links
                          for entry in sublist
                          if 'noagendanotes' in entry]

        # visit opml for each link pointed to
        responses = [r for r in get_pages(shownote_links)]
        opmls = [x.url.replace('html', 'opml') for x in responses]

        for opml in opmls:
            self.stdout.write('Loading {}'.format(opml))
            try:
                loader = OpmlLoader(opml)
                loader.save()
                self.stdout.write('opml parsed for episode {}'.format(loader.number))
            except Exception as e:
                self.stdout.write('Error occured while loading opml: {}'.format(e))
