from django.db import models


class Show(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return '{}: {}'.format(self.id, self.name)


class Note(models.Model):
    show = models.ForeignKey(Show)
    topic = models.CharField(max_length=100)
    title = models.TextField()

    def __unicode__(self):
        return '{} [{}]: {}'.format(
            self.topic, self.show.id, self.title[:20])


class TextEntry(models.Model):
    note = models.ForeignKey(Note)
    text = models.TextField()

    def __unicode__(self):
        return '{}: {}'.format('text', self.text[:20])


class UrlEntry(models.Model):
    note = models.ForeignKey(Note)
    text = models.TextField()
    url = models.TextField()

    def __unicode__(self):
        return '{}: {}'.format('url', self.text[:20])
