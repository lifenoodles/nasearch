from django.db import models


class Show(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    last_updated = models.DateTimeField()

    def __unicode__(self):
        return '{}: {}'.format(self.id, self.name)


class Entry(models.Model):
    show = models.ForeignKey(Show)
    topic = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    title = models.TextField()
    content = models.TextField()

    def __unicode__(self):
        return '{} [{}]: {}'.format(
            self.topic, self.type, self.content[:20])
