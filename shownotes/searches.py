from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery
from shownotes.models import Show
from django.db.models import Max


def search(string, topics, min_show=0, max_show=None):
    if max_show is None:
        max_show = Show.objects.all().aggregate(Max('id'))['id__max']
    if string == '':
        return SearchQuerySet().filter(
            topic_id__in=topics, id__gte=min_show, id__lte=max_show) \
            .order_by('-show_number').order_by('topic_name')
    else:
        return SearchQuerySet().filter(
            SQ(text=AutoQuery(string)), topic_id__in=topics,
            id__gte=min_show, id__lte=max_show)


def topics_in_show(number):
    return SearchQuerySet().filter(show_number=number).order_by('topic_name')
