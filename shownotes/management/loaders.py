import opml
import common.netutils as netutils
from datetime import datetime
from shownotes.models import Show, Note, TextEntry, UrlEntry


def opml_from_shownotes(*urls):
    '''
    returns a list of opml files corresponding to the given
    shownote url
    '''
    responses = [r for r in netutils.get_pages(*urls)]
    opmls = [x.url.replace('html', 'opml') for x in responses]
    return opmls


class OpmlSourceError(Exception):
    pass


class OpmlLoader(object):
    def __init__(self, source):
        self.source = source
        try:
            self.data = opml.parse(source)
        except Exception as e:
            raise OpmlSourceError(e)
        try:
            self.number = self._show_number()
            # we need an explicit copy here so we get the unicode str
            self.title = self.data.title[:]
        except ValueError:
            raise ValueError('Bad opml data, no show number')

    def save(self):
        if self.exists():
            show = Show.objects.get(pk=self.number)
            if self.date_modified() > show.last_updated:
                show.delete()
        if not self.exists():
            self._insert_show()
            self._insert_entries()

    def date_modified(self):
        try:
            date_string = self.data.dateModified
            return datetime.strptime(
                date_string, '%a, %d %b %Y %H:%M:%S %Z')
        except ValueError:
            return datetime.fromtimestamp(0)

    def exists(self):
        return Show.objects.filter(pk=self.number).count() == 1

    def _show_number(self):
        numbers = self.data.title.split()
        numbers = filter(lambda x: x.isdigit(), numbers)
        if len(numbers) == 0:
            raise ValueError
        return int(numbers[0])

    def _delete_show(self):
        assert self.exists()
        Show.objects.get(pk=self.number).delete()
        assert not self.exists()

    def _insert_show(self):
        assert not self.exists()
        show = Show(name=self.title, id=self.number,
                    last_updated=self.date_modified())
        show.save()
        assert self.exists()

    def _get_shownotes(self):
        for v in self.data[1]:
            if v.text == 'Shownotes':
                return v
        raise ValueError('No Shownotes Found')

    def _insert_entries(self):
        assert self.exists()
        show = Show.objects.get(pk=self.number)
        shownotes = self._get_shownotes()
        for topic in shownotes:
            if len(topic) == 0:
                continue
            topic_name = topic.text
            for note in topic:
                if len(note) == 0:
                    continue
                new_note = Note(
                    show=show, topic=topic_name,
                    title=note.text)
                new_note.save()
                full_text = []
                for entry in note:
                    if hasattr(entry, 'type'):
                        new_entry = UrlEntry(
                            note=new_note,
                            text=entry.text,
                            url=entry.url)
                        new_entry.save()
                    else:
                        full_text.append(entry.text)
                new_entry = TextEntry(
                    note=new_note, text='\n'.join(full_text))
                new_entry.save()
