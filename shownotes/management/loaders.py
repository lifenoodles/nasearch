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


class OpmlParser(object):
    def __init__(self, source):
        self.source = source
        self.show = Show()
        self.notes = []
        self.text_entries = []
        self.url_entries = []
        try:
            self.data = opml.parse(source)
        except Exception as e:
            raise OpmlSourceError(e)
        self._construct_show()

    def construct_models(self):
        shownotes = self._get_shownotes()
        for topic in shownotes:
            if len(topic) == 0:
                continue
            topic_name = topic.text
            for note in topic:
                if len(note) == 0:
                    continue
                new_note = Note(
                    show=self.show, topic=topic_name,
                    title=note.text)
                self.notes.append(new_note)
                full_text = []
                for entry in note:
                    if hasattr(entry, 'type'):
                        new_entry = UrlEntry(
                            note=new_note,
                            text=entry.text,
                            url=entry.url)
                        self.url_entries.append(new_entry)
                    else:
                        full_text.append(entry.text)
                new_entry = TextEntry(
                    note=new_note, text='\n'.join(full_text))
                self.text_entries.append(new_entry)

    def _construct_show(self):
        try:
            # we need an explicit copy here so we get the unicode str
            self.show = Show(
                id=self._show_number(),
                name=self.data.title[:],
                last_updated=self._date_modified())
        except ValueError:
            raise ValueError('Bad opml data, no show number')

    def _date_modified(self):
        try:
            date_string = self.data.dateModified
            return datetime.strptime(
                date_string, '%a, %d %b %Y %H:%M:%S %Z')
        except ValueError:
            return datetime.fromtimestamp(0)

    def _show_number(self):
        numbers = self.data.title.split()
        numbers = filter(lambda x: x.isdigit(), numbers)
        if len(numbers) == 0:
            raise ValueError
        return int(numbers[0])

    def _get_shownotes(self):
        for v in self.data[1]:
            if v.text == 'Shownotes':
                return v
        raise ValueError('No Shownotes Found')


class OpmlLoader(object):
    def __init__(self, source):
        self.parser = OpmlParser(source)
        self.show_id = self.parser.show.id

    def save(self):
        if Show.objects.filter(id=self.parser.show.id).exists():
            old_show = Show.objects.get(pk=self.parser.show.id)
            if self.parser.show.last_updated > old_show.last_updated:
                show.delete()
        if not Show.objects.filter(id=self.parser.show.id).exists():
            self.parser.construct_models()
            self.parser.show.save()
            # print repr(self.parser.show)
            for note in self.parser.notes:
                note.save()
                # print note
            for entry in self.parser.url_entries:
                entry.save()
                # print entry
            for entry in self.parser.text_entries:
                entry.save()
                # print entry
