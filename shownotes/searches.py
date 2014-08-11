from shownotes.models import Topic, Note, UrlEntry, TextEntry
from django.core.paginator import Paginator, EmptyPage
from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery


def topics():
    return [{'text': t.name, 'id': t.id} for t in Topic.objects.all()]


def search(parameters):
    RESULTS_LIMIT = 50
    TOPIC_LIMIT = 10
    topics = []
    if 'topics' in parameters:
        topics = [int(t) for t in parameters['topics'].split() if t.isdigit()]
    topics = topics[:TOPIC_LIMIT]
    limit = RESULTS_LIMIT
    if 'limit' in parameters and parameters['limit'].isdigit():
        limit = min(RESULTS_LIMIT, int(parameters['limit']))
    page = 1
    if 'page' in parameters and parameters['page'].isdigit():
        page = int(parameters['page'])
    string = ''
    if 'string' in parameters:
        string = parameters['string']

    response_dict = {'results': [], 'page': 0, 'page_count': 0,
                     'result_count': 0, 'page_result_count': 0}
    if string == '' and topics == []:
        return response_dict

    if string == '':
        results = SearchQuerySet().filter(topic_id__in=topics) \
            .order_by('-show_number').order_by('topic_name')
    else:
        results = SearchQuerySet().filter(topic_id__in=topics) \
            .filter(SQ(text=AutoQuery(string)) |
                    SQ(text_entry=AutoQuery(string)))

    response_dict['result_count'] = results.count()
    paginator = Paginator(results, limit)
    response_dict['page_count'] = paginator.num_pages
    try:
        paged_results = paginator.page(page)
        response_dict['page'] = page
    except EmptyPage:
        paged_results = []
        response_dict['page'] = 0
    response_dict['results'] = [json_result(x) for x in paged_results]
    response_dict['page_result_count'] = len(paged_results)
    return response_dict


def show(number):
    return SearchQuerySet().filter(show_number=number).order_by('topic_name')
