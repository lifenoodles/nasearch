from shownotes.models import Show, ShowSource
from django.core.management.base import BaseCommand
import shownotes.management.loaders as loaders
import common.netutils as netutils
from collections import deque
from threading import Thread
import time
import re

HTML_LIST = deque()
SHOWNOTE_MID_CUTOFF = 490
SHOWNOTE_CUTOFF = 375
NEW_HTML_FORMAT_START = 590
# SHOWNOTE_CUTOFF = 505
BAD_LIST = [534, 533, 505]


def html_getter(*show_number):
    show_number = show_number[0]
    direct_cutoff = SHOWNOTE_MID_CUTOFF
    main_url = 'http://{}.nashownotes.com'
    shownote_url = 'http://{}.nashownotes.com/shownotes'
    for number in reversed(xrange(SHOWNOTE_CUTOFF, show_number + 1)):
        if number in BAD_LIST:
            continue
        if not Show.exists(number):
            if ShowSource.exists(number):
                HTML_LIST.append(number)
                continue
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
            opml_links = netutils.get_links_to('^http://.*\.opml$', text)
            if len(opml_links) > 0:
                assert(len(opml_links) == 1)
                try:
                    opml = netutils.get_html(opml_links[0])
                except:
                    print('Error loading opml from: {}'.format(
                        opml_links[0]))
                    continue
                print('   -> {} opml'.format(number))
                ShowSource(filetype=ShowSource.OPML, text=opml,
                           show_number=number).save()
                HTML_LIST.append(number)
            else:
                print('   -> {} html'.format(number))
                ShowSource(filetype=ShowSource.HTML, text=text,
                           show_number=number).save()
                HTML_LIST.append(number)
            time.sleep(0.01)
        else:
            print('Show {} already imported'.format(number))


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

        html_thread = Thread(target=html_getter, args=(show_number,))
        html_thread.start()

        while html_thread.is_alive() or len(HTML_LIST) > 0:
            try:
                number = HTML_LIST.popleft()
            except IndexError:
                time.sleep(0.01)
                continue

            assert ShowSource.exists(number)
            source = ShowSource.objects.get(show_number=number)
            if source.filetype == ShowSource.OPML:
                self.stdout.write('loading opml for show {}'.format(number))
                try:
                    loader = loaders.OpmlLoader(source.text)
                    loader.save()
                    self.stdout.write('opml parsed for show {}'
                                      .format(loader.number))
                except Exception as e:
                    self.stdout.write(
                        'Error occured while loading opml: {}'
                        .format(e))
            else:
                self.stdout.write('loading html for show {}'.format(number))
                try:
                    if number >= NEW_HTML_FORMAT_START:
                        loader = loaders.NewHtmlLoader(source.text, number)
                    else:
                        loader = loaders.HtmlLoader(source.text, number)
                    loader.save()
                    self.stdout.write('html parsed for episode {}'
                                      .format(number))
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    # self.stdout.write(
                    #     'Error occured while loading html: {}'
                    #     .format(e))
