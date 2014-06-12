from django.core.management.base import BaseCommand
from shownotes.models import Show
from shownotes.management.loaders import OpmlLoader
import shownotes.management.loaders as loaders
import common.netutils as netutils
import requests
import opml
import re


number_pattern = re.compile('(\d+)')


def show_number(string):
    match = number_pattern.search(string)
    if match:
        return int(match.group())
    return None


def handle_opml_link(url):
    try:
        loader = OpmlLoader(url)
        loader.save()
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


def handle_html(url):
    pass


def handle_redirect(url):
    if url.endswith('html'):
        return
        # pull down the url
        response = requests.get(url)
        if response.status_code == 200:
            links = netutils.extract_urls_from_html(response.text)
            links = [link for link in links if link.endswith('.opml')]
            if len(links) > 0:
                handle_opml_link(links[0])
                print('handled opml file: {}'.format(links[0]))
            else:
                handle_html(response.text)
                print('handled html file: {}'.format(url))
        else:
            print('Bad response from: {}'.format(url))
    elif url.endswith('opml'):
        handle_opml_link(url)
        print('Imported opml file: {}'.format(url))
    else:
        # print('IGNORED {}'.format(url))
        pass


class Command(BaseCommand):
    help = 'Attempt to fetch updates from the archive opml file.'
    NA_RSS_URL = 'http://feed.nashownotes.com/'

    def handle(self, *args, **options):
        archive = opml.parse('na-archive.opml')
        shows = [show for year in archive
                 for month in year for show in month]
        for show in shows:
            number = show_number(show.text)
            if number and not Show.objects.filter(id=number):
                if not hasattr(show, 'type'):
                    continue
                # print('Handling {} [{}]'.format(show.url, number))
                handle_redirect(show.url)
