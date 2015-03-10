import unittest
from datetime import datetime
from shownotes.models import Show, Topic, Note, TextEntry, UrlEntry


class ShowTest(unittest.TestCase):
    def test_no_show_exists(self):
        self.assertIs(Show.exists(1), False)

    def test_show_to_unicode(self):
        show = Show(id=7, name='showname', last_updated=datetime.now())
        self.assertEqual(unicode(show), u'7: showname')

    def test_show_exists(self):
        Show(id=7, name='showname', last_updated=datetime.now()).save()
        self.assertIs(Show.exists(7), True)


class TopicTest(unittest.TestCase):
    def setUp(self):
        set_up_database()

    def tearDown(self):
        tear_down_database()

    def test_notes_to_retrieve(self):
        self.assertEqual(Topic.objects.get(id=1).note_count(), 3)
        self.assertEqual(Topic.objects.get(id=2).note_count(), 0)
        self.assertEqual(Topic.objects.get(id=3).note_count(), 0)

    def test_topic_to_unicode(self):
        self.assertEqual(unicode(Topic.objects.get(id=1)), u'topic name')

    def test_get_by_id(self):
        self.assertEqual(len(Topic.get_by_id()), 0)
        self.assertEqual(len(Topic.get_by_id(2)), 1)
        self.assertEqual(len(Topic.get_by_id(1, 3)), 2)
        self.assertEqual(len(Topic.get_by_id(1, 2, 3)), 3)
        self.assertEqual(len(Topic.get_by_id(1, 2, 3, 4)), 3)

    def test_exists(self):
        self.assertEqual(Topic.exists('topic name'), True)
        self.assertEqual(Topic.exists('no topic'), False)


class NoteTest(unittest.TestCase):
    def setUp(self):
        set_up_database()

    def tearDown(self):
        tear_down_database()

    def test_text_entry(self):
        self.assertEqual(Note.objects.get(id=1).text_entry(), 'text entry 1')
        self.assertEqual(Note.objects.get(id=2).text_entry(), 'text entry 3')
        self.assertEqual(Note.objects.get(id=3).text_entry(), '')

    def test_urls(self):
        urls = UrlEntry.objects.filter(id__lte=3)
        self.assertItemsEqual(Note.objects.get(id=1).urls(), urls)
        urls = UrlEntry.objects.filter(id__gt=3).filter(id__lte=4)
        self.assertItemsEqual(Note.objects.get(id=2).urls(), urls)
        self.assertItemsEqual(Note.objects.get(id=3).urls(), [])

    def test_unicode(self):
        note = Note.objects.get(id=1)
        self.assertEqual(unicode(note), u'topic name [1]: note 1')

    def test_get_by_topic(self):
        topic = Topic.objects.get(id=1)
        notes = Note.objects.filter(topic=topic)
        self.assertItemsEqual(Note.get_by_topic(topic), notes)


class TextEntryTest(unittest.TestCase):
    def setUp(self):
        set_up_database()

    def tearDown(self):
        tear_down_database()


def set_up_database():
    show = Show(id=1, name='show name', last_updated=datetime.now())
    show.save()
    for i in xrange(1, 4):
        Topic(id=i, name='topic name').save()
    topic = Topic.objects.get(id=1)

    note = Note(id=1, show=show, topic=topic, title='note 1')
    note.save()
    TextEntry(note=note, text='text entry 1').save()
    TextEntry(note=note, text='text entry 2').save()
    UrlEntry(id=1, note=note, text='url text 1', url='http://foo.com').save()
    UrlEntry(id=2, note=note, text='url text 2', url='http://bar.com').save()
    UrlEntry(id=3, note=note, text='url text 3', url='http://baz.com').save()

    note = Note(id=2, show=show, topic=topic, title='note 2')
    note.save()
    TextEntry(note=note, text='text entry 3').save()
    UrlEntry(id=4, note=note, text='url text 4', url='http://foo.com').save()

    note = Note(id=3, show=show, topic=topic, title='note 3')
    note.save()


def tear_down_database():
    Show.objects.get(id=1).delete()
