import unittest
from datetime import datetime
from shownotes.models import Show, Topic, Note, TextEntry, UrlEntry


class ShowTest(unittest.TestCase):
    def test_no_show_exists(self):
        self.assertIs(Show.exists(1), False)

    def test_show_to_unicode(self):
        show = Show(id=7, name='showname', last_updated=datetime.now())
        self.assertEquals(unicode(show), u'7: showname')

    def test_show_exists(self):
        Show(id=7, name='showname', last_updated=datetime.now()).save()
        self.assertIs(Show.exists(7), True)


class TopicTest(unittest.TestCase):
    def setUp(self):
        show = Show(id=1, name='show name', last_updated=datetime.now())
        show.save()
        for i in xrange(1, 4):
            Topic(id=i, name='topic name').save()
        topic = Topic.objects.get(id=1)
        for i in xrange(1, 4):
            Note(show=show, topic=topic, title='note title').save()

    def tearDown(self):
        Show.objects.get(id=1).delete()

    def test_notes_to_retrieve(self):
        self.assertEquals(Topic.objects.get(id=1).note_count(), 3)
        self.assertEquals(Topic.objects.get(id=2).note_count(), 0)
        self.assertEquals(Topic.objects.get(id=3).note_count(), 0)

    def test_topic_to_unicode(self):
        self.assertEquals(unicode(Topic.objects.get(id=1)), u'topic name')

    def test_get_by_id(self):
        self.assertEquals(len(Topic.get_by_id()), 0)
        self.assertEquals(len(Topic.get_by_id(2)), 1)
        self.assertEquals(len(Topic.get_by_id(1, 3)), 2)
        self.assertEquals(len(Topic.get_by_id(1, 2, 3)), 3)
        self.assertEquals(len(Topic.get_by_id(1, 2, 3, 4)), 3)

    def test_exists(self):
        self.assertEquals(Topic.exists('topic name'), True)
        self.assertEquals(Topic.exists('no topic'), False)


class NoteTest(unittest.TestCase):
    def setUp(self):
        prepare_database()

    def tearDown(self):
        clean_database()

    def test_text_entry(self):
        self.assertEquals(Note.objects.get(id=1).text_entry(), 'text entry 1')


def prepare_database():
    show = Show(id=1, name='show name', last_updated=datetime.now())
    show.save()
    for i in xrange(1, 4):
        Topic(id=i, name='topic name').save()
    topic = Topic.objects.get(id=1)

    note = Note(id=1, show=show, topic=topic, title='note 1')
    note.save()
    TextEntry(note=note, text='text entry 1').save()
    TextEntry(note=note, text='text entry 2').save()
    UrlEntry(note=note, text='url text 1', url='http://foo.com').save()
    UrlEntry(note=note, text='url text 2', url='http://bar.com').save()
    UrlEntry(note=note, text='url text 3', url='http://baz.com').save()

    note = Note(id=2, show=show, topic=topic, title='note 2')
    note.save()
    TextEntry(note=note, text='text entry 1').save()
    UrlEntry(note=note, text='url text 1', url='http://foo.com').save()

    note = Note(id=3, show=show, topic=topic, title='note 3')
    note.save()


def clean_database():
    Show.objects.get(id=1).delete()
