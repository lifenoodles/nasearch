from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery
from shownotes.models import Show
from django.db.models import Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search(string, topics, min_show=0, max_show=None):
    if max_show is None:
        max_show = Show.objects.all().aggregate(Max('id'))['id__max']
    print max_show
    if string == '':
        return SearchQuerySet().filter(
            topic_id__in=topics, show_number__gte=min_show,
            show_number__lte=max_show).order_by('-show_number', 'topic_name')
    else:
        return SearchQuerySet().filter(
            SQ(text=AutoQuery(string)), topic_id__in=topics,
            show_number__gte=min_show, show_number__lte=max_show)


def paginate(results, page, limit):
    paginator = Paginator(results, limit)
    try:
        paged_results = paginator.page(page)
        return (paged_results, page, paginator.num_pages)
    except EmptyPage:
        return ([], 1, 1)
    except PageNotAnInteger:
        return (paginator.page(1), 1, paginator.num_pages)


def topics_in_show(number):
    return SearchQuerySet().filter(show_number=number).order_by('topic_name')
