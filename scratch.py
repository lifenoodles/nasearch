import re
from BeautifulSoup import BeautifulSoup
import requests

matcher = re.compile('.*Shownotes*.')
soup = BeautifulSoup(requests.get('http://375.nashownotes.com/').text)
shownote_div = soup.find(id=matcher)
list_div = shownote_div.find('div', {'class': 'divOutlineList'})
topics = [e for e in list_div.childGenerator()
          if hasattr(e, 'findChild') and e.text != u'Search']

i = 0
while i < len(topics):
    topic = topics[i].text

    notes = topics[i + 1].find('div', {'class': 'divOutlineList'}) \
        .findChildren('p', recursive=False)

    print u'TOPIC: {}'.format(topic)
    for note in notes:
        next_sibling = note.findNextSibling()
        if next_sibling is None or next_sibling.name != u'div':
            continue

        print u'NOTE: {}'.format(note.text)
        contents = note.findNextSibling('div').findChildren(
            '', {'class': 'divOutlineItem'})
        text = []
        for content in contents:
            link = content.findChild('a')
            if link:
                text.append(u'LINK: {}'.format(link.text))
            else:
                text.append(content.text)
        print u'CONTENTS: {}'.format('\n'.join(text))

    i += 2
