from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery
import json


TOPIC_SEARCH_LIMIT = 10
RESULTS_SEARCH_LIMIT = 20


def index(request):
    return render(request, 'shownotes/index.html')


def search_topics(request):
    if 'string' in request.GET \
            and 'topics' in request.GET \
            and 'page' in request.GET:
        results = []
        topic_ids = [int(t) for t in request.GET['topics'].split()]
        context = {}
        response_dict = {'page': 0, 'page_count': 0}

        if len(topic_ids) > TOPIC_SEARCH_LIMIT:
            context['limit'] = TOPIC_SEARCH_LIMIT
            topic_ids = topic_ids[:TOPIC_SEARCH_LIMIT]

        if request.GET['string'] == '':
            if len(topic_ids) == 0:
                response_dict['html'] = render_to_string(
                    'shownotes/empty-topic.html')
                return HttpResponse(json.dumps(response_dict),
                                    content_type='application/json')

            results = SearchQuerySet().filter(topic_id__in=topic_ids) \
                .order_by('show_number').order_by('topic_name')
        else:
            query = request.GET['string']
            print topic_ids
            results = SearchQuerySet().filter_and(
                SQ(text=AutoQuery(query)), topic_id__in=topic_ids)

        context['matches'] = len(results)
        paginator = Paginator(results, RESULTS_SEARCH_LIMIT)
        response_dict['page_count'] = paginator.num_pages
        try:
            results = paginator.page(request.GET['page'])
            response_dict['page'] = int(request.GET['page'])
        except PageNotAnInteger:
            results = paginator.page(1)
            response_dict['page'] = 1
        except EmptyPage:
            results = []
            response_dict['page'] = paginator.num_pages

        context['results'] = results
        if request.GET['page'] == '1':
            response_dict['html'] = render_to_string(
                'shownotes/topic-container.html', context)
        else:
            response_dict['html'] = render_to_string(
                'shownotes/topic-list.html', context)
        return HttpResponse(json.dumps(response_dict),
                            content_type='application/json')
    else:
        html = render_to_string(
            'shownotes/topic-container.html')
        return HttpResponse(json.dumps({'page': '0',
                                        'page_count': '0',
                                        'html': html}),
                            content_type='application/json')
