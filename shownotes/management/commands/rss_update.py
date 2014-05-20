from django.core.management.base import BaseCommand
import shownotes.management.loaders as loaders
import common.netutils as netutils


class Command(BaseCommand):
    help = 'Fetches updates from the no agenda rss feed'
    NA_RSS_URL = 'http://feed.nashownotes.com/'

    def handle(self, *args, **options):
        feed = netutils.get_rss_feed(Command.NA_RSS_URL)

        shownote_links = filter(lambda x: 'noagendanotes' in x,
                                netutils.extract_urls_from_rss(feed))

        opmls = loaders.opml_from_shownotes(*shownote_links)

        # visit opml for each link pointed to
        for opml in opmls:
            self.stdout.write('Loading {}'.format(opml))
            # try:
            loader = loaders.OpmlLoader(opml)
            loader.save()
            self.stdout.write('opml parsed for episode {}'
                              .format(loader.number))
            # except Exception as e:
            #     self.stdout.write('Error occured while loading opml: {}'
            #                       .format(e))
