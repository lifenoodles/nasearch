from shownotes.models import Topic
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Merges topics that are meant to be the same
              prior to index building'''
    BAD_TOPICS = []

    def delete_empty_topics(self):
        unused_topics = [t for t in Topic.objects.all()
                         if t.note_count() == 0]
        for topic in unused_topics:
            topic.delete()

    def delete_bad_topics(self):
        for topic in Topic.objects.filter(name__in=Command.BAD_TOPICS):
            topic.delete()

    def handle(self, *args, **options):
        self.delete_empty_topics()
        self.delete_bad_topics()
