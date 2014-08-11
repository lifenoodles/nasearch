from shownotes.models import Topic, Note, UrlEntry, TextEntry
from django.core.paginator import Paginator, EmptyPage
from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery


def search(string, topics):
    if string == '':
        results = SearchQuerySet().filter(topic_id__in=topics) \
            .order_by('-show_number').order_by('topic_name')
    else:
        results = SearchQuerySet().filter(topic_id__in=topics) \
            .filter(SQ(text=AutoQuery(string)) |
                    SQ(text_entry=AutoQuery(string)))
    return results


def topics_in_show(number):
    return SearchQuerySet().filter(show_number=number).order_by('topic_name')
