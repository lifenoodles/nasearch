from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery


def search(string, topics):
    if string == '':
        return SearchQuerySet().filter(topic_id__in=topics).order_by(
            '-show_number').order_by('topic_name')
    else:
        return SearchQuerySet().filter(
            SQ(text=AutoQuery(string)),
            topic_id__in=topics)


def topics_in_show(number):
    return SearchQuerySet().filter(show_number=number).order_by('topic_name')
