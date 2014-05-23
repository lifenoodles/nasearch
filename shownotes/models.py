from django.db import models
from django.db.models import Q


class Show(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return u'{}: {}'.format(self.id, self.name)


class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_by_id(cls, *ids):
        if len(ids) == 0:
            return []
        qs = [Q(id=x) for x in ids]
        query = reduce(lambda x, y: x | y, qs)
        return Topic.objects.filter(query)


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

    def text_web(self):
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
