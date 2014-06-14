from shownotes.models import Show
from django.core.management.base import BaseCommand
import shownotes.management.loaders as loaders
import common.netutils as netutils
import re
from collections import deque
from threading import Thread
import time

html_list = deque()
SHOWNOTE_MID_CUTOFF = 490
# SHOWNOTE_CUTOFF = 375
SHOWNOTE_CUTOFF = 490


def html_getter(*show_number):
    show_number = show_number[0]
    direct_cutoff = SHOWNOTE_MID_CUTOFF
    main_url = 'http://{}.nashownotes.com'
    shownote_url = 'http://{}.nashownotes.com/shownotes'
    for number in reversed(xrange(SHOWNOTE_CUTOFF, show_number + 1)):
        if not Show.exists(number):
            if number < direct_cutoff:
                url = shownote_url.format(number)
            else:
                url = main_url.format(number)

            try:
                text = netutils.get_html(url)
            except:
                print('Error loading html from: {}'.format(url))
                continue

            # check for opml links
            opml_links = netutils.get_links_to('$http://.*\.opml$', text)
            if len(opml_links) > 0:
                assert(len(opml_links) == 1)
                print('   -> {} opml'.format(number))
                html_list.append((number, opml_links[0]))
            else:
                print('   -> {} html'.format(number))
                html_list.append((number, text))
        else:
            print('Show {} already exists'.format(number))


class Command(BaseCommand):
    help = 'Fetches shownotes for all episodes from the most recent back'
    NA_RSS_URL = 'http://feed.nashownotes.com/'

    def handle(self, *args, **options):
        # feed = netutils.get_rss_feed(Command.NA_RSS_URL)

        # shownote_links = [x for x in
        #                   netutils.extract_urls_from_rss(feed)
        #                   if 'noagendanotes' in x]

        # regex = '\\d+'
        # numbers = [re.search(regex, x) for x in shownote_links]
        # numbers = [x.string[x.start():x.end()] for x in numbers
        #            if x is not None]
        # show_number = max([int(x) for x in numbers])

        html_thread = Thread(target=html_getter, args=(554,))
        html_thread.start()

        while html_thread.is_alive() or len(html_list) > 0:
            try:
                number, text = html_list.popleft()
            except IndexError:
                time.sleep(0.1)
                continue

            if re.search('^http://.*\.opml$', text):
                self.stdout.write('Loading {}'.format(text))
                try:
                    loader = loaders.OpmlLoader(text)
                    loader.save()
                    self.stdout.write('opml parsed for episode {}'
                                      .format(loader.number))
                except Exception as e:
                    self.stdout.write(
                        'Error occured while loading opml: {}'
                        .format(e))
            else:
                self.stdout.write('Loading html for show {}'.format(number))
                try:
                    loader = loaders.HtmlLoader(text, number)
                    loader.save()
                    self.stdout.write('html parsed for episode {}'
                                      .format(number))
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    # self.stdout.write(
                    #     'Error occured while loading html: {}'
                    #     .format(e))
