from django.db import models
from django.db.models import Q


class Show(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.name)

    @classmethod
    def exists(cls, number):
        return Show.objects.filter(pk=number).count() == 1


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def note_count(self):
        return Note.objects.filter(topic__id=self.id).count()

    def __unicode__(self):
        return self.name

    @classmethod
    def get_by_id(cls, *ids):
        if len(ids) == 0:
            return []
        qs = [Q(id=x) for x in ids]
        query = reduce(lambda x, y: x | y, qs)
        return Topic.objects.filter(query)

    @classmethod
    def exists(cls, name):
        return Topic.objects.filter(name=name).count() > 0


class Note(models.Model):
    show = models.ForeignKey(Show)
    topic = models.ForeignKey(Topic)
    title = models.TextField()

    def __unicode__(self):
        return u'{} [{}]: {}'.format(
            self.topic, self.show.id, self.title[:20])

    @classmethod
    def get_by_topic(cls, topic):
        return Note.objects.filter(topic=topic)


class TextEntry(models.Model):
    note = models.ForeignKey(Note)
    text = models.TextField()

    def text_html(self):
        return self.text.replace('\n', '<br>')

    def __unicode__(self):
        return u'{}: {}'.format('text', self.text[:20])

    @classmethod
    def get_by_note(cls, note):
        return TextEntry.objects.filter(note=note)


class UrlEntry(models.Model):
    note = models.ForeignKey(Note)
    text = models.TextField()
    url = models.TextField()

    def link(self):
        return u'<a href={}>{}</a>'.format(self.url, self.url)

    def __unicode__(self):
        return u'{}: {}'.format('url', self.text[:20])

    @classmethod
    def get_by_note(cls, note):
        return UrlEntry.objects.filter(note=note)


class ShowSource(models.Model):
    OPML = 'opml'
    HTML = 'html'
    SOURCE_CHOICES = ((OPML, 'opml'), (HTML, 'html'))
    filetype = models.CharField(max_length=4, choices=SOURCE_CHOICES)
    text = models.TextField()
    show_number = models.IntegerField(unique=True)

    @classmethod
    def exists(cls, number):
        return ShowSource.objects.filter(show_number=number).count() == 1
