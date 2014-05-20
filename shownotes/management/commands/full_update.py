from django.core.management.base import BaseCommand
import shownotes.management.loaders as loaders
import common.netutils as netutils
import re


class Command(BaseCommand):
    help = 'Fetches shownotes for all episodes from the most recent back'
    NA_RSS_URL = 'http://feed.nashownotes.com/'

    def handle(self, *args, **options):
        feed = netutils.get_rss_feed(Command.NA_RSS_URL)

        shownote_links = [x for x in
                          netutils.extract_urls_from_rss(feed)
                          if 'noagendanotes' in x]

        regex = '\\d+'
        numbers = [re.search(regex, x) for x in shownote_links]
        numbers = [x.string[x.start():x.end()] for x in numbers
                   if x is not None]
        show_number = max([int(x) for x in numbers])

        url_pattern = 'http://{}.noagendanotes.com'
        for number in reversed(xrange(1, show_number + 1)):
            url = url_pattern.format(number)
            opmls = loaders.opml_from_shownotes(url)
            for opml in opmls:
                self.stdout.write('Loading {}'.format(opml))
                try:
                    loader = loaders.OpmlLoader(opml)
                    loader.save()
                    self.stdout.write('opml parsed for episode {}'
                                      .format(loader.number))
                except Exception as e:
                    self.stdout.write(
                        'Error occured while loading opml: {}'
                        .format(e))
