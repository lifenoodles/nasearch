from shownotes.models import Topic
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Merges topics that are meant to be the same
              prior to index building'''
    TOPIC_LISTS = [
        (['99 Fists', '99Fists'], '99 Fists'),
        (['99 Fists', '99Fists'], '99 Fists')
    ]

    def clean_empty_topics():
        unused_topics = [t for t in Topic.all() if t.note_count() == 0]
        for topic in unused_topics:
            topic.delete()

    def handle(self, *args, **options):
        self.clean_empty_topics()
        for tlist, name in Command.TOPIC_LISTS:
            pass
