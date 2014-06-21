from shownotes.models import ShowSource
from django.core.management.base import BaseCommand
import shownotes.management.loaders as loaders
import common.netutils as netutils
import re


class Command(BaseCommand):
    help = 'Fetches updates from the no agenda rss feed'
    NA_RSS_URL = 'http://feed.nashownotes.com/'

    def handle(self, *args, **options):
        feed = netutils.get_rss_feed(Command.NA_RSS_URL)

        shownote_links = filter(lambda x: 'noagendanotes' in x,
                                netutils.extract_urls_from_rss(feed))
        number_re = re.compile('\d+')

        def shownote_filter(url):
            match = number_re.search(url)
            if match:
                number = match.group()
                if ShowSource.exists(number):
                    return False
                return True
            else:
                return False

        shownote_links = [s for s in shownote_links if shownote_filter(s)]
        for link in shownote_links:
            print link
            number = number_re.search(link).group()
            try:
                netutils.insert_show_source(
                    link, number)
                loaders.load_shownotes(number)
            except:
                print('Error updating shownotes:')
                import traceback
                traceback.print_exc()
