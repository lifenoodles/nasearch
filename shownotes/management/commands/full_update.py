from models import Show
from django.core.management.base import BaseCommand
import shownotes.management.loaders as loaders
import common.netutils as netutils
import re
from collections import deque
from threading import Thread
import time

html_list = deque()


def html_getter(*show_number):
    show_number = show_number[0]
    direct_cutoff = 490
    main_url = 'http://{}.nashownotes.com'
    shownote_url = 'http://{}.nashownotes.com/shownotes'
    for number in reversed(xrange(375, show_number + 1)):
        if Show.exists(number):
            if number < direct_cutoff:
                url = main_url.format(number)
            else:
                shownote_url.format(number)

            try:
                text = netutils.get_html()
            except:
                print('Error loading html from: {}'.format(url))
                continue

            # check for opml links
            opml_links = netutils.get_links_to('.opml$', text)
            if len(opml_links) > 0:
                assert(len(opml_links == 1))
                print('Inserting opml for show: {}'.format(number))
                html_list.append((number, opml_links[0]))
            else:
                print('Inserting html for show: {}'.format(number))
                html_list.append((number, text))
        else:
            print('Show {} already exists'.format(number))


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
        html_thread.run()

        while html_thread.is_alive():
            try:
                number, text = deque.pop()
            except IndexError:
                time.sleep(0.1)

            if re.search('http://.*\.opml', text):
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
                    self.stdout.write(
                        'Error occured while loading html: {}'
                        .format(e))


if __name__ == '__main__':
    import bs4
    import requests

    matcher = re.compile('.*Shownotes*.')
    soup = bs4.BeautifulSoup(requests.get('http://489.nashownotes.com/'))
    shownote_div = soup.find(id=matcher)
    list_div = shownote_div.find('div', {'class': 'divOutlineList'})
