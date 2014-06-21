from shownotes.models import Topic
from django.core.management.base import BaseCommand
from django.utils.html import strip_tags


class Command(BaseCommand):
    help = '''Merges topics that are meant to be the same
              prior to index building'''
    BAD_TOPICS = [
        '<a href="http://search.nashownotes.com">Search</a>'
    ]

    def delete_empty_topics(self):
        unused_topics = [t for t in Topic.objects.all()
                         if t.note_count() == 0]
        for topic in unused_topics:
            topic.delete()

    def delete_bad_topics(self):
        for topic in Topic.objects.filter(name__in=Command.BAD_TOPICS):
            topic.delete()

    def clean_topic_names(self):
        for topic in Topic.objects.all():
            topic.name = strip_tags(topic.name)
            topic.save()

    def handle(self, *args, **options):
        self.delete_empty_topics()
        self.delete_bad_topics()
