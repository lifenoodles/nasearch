from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models import Max, Min
from shownotes.models import Show
import json
import searches


TOPIC_SEARCH_LIMIT = 10
RESULTS_SEARCH_LIMIT = 20


def index(request):
    agg = Show.objects.all().aggregate(Max('id'), Min('id'))
    context = {'show_numbers':
               [x for x in range(agg['id__min'], agg['id__max'] + 1)]}
    print context
    return render(request, 'shownotes/index.html', context)


def search_topics(request):
    """
    perform a search and return the matches
    """
    topics = []
    if 'topics' in request.GET:
        topics = [int(t) for t in request.GET['topics'].split() if t.isdigit()]
    string = ''
    if 'string' in request.GET:
        string = request.GET['string']
    min_show = 0
    if 'min_show' in request.GET and request.GET['min_show'].isdigit():
        min_show = int(request.GET['min_show'])
    max_show = None
    if 'max_show' in request.GET and request.GET['max_show'].isdigit():
        max_show = int(request.GET['max_show'])
    page = 1
    if 'page' in request.GET and request.GET['page'].isdigit():
        page = int(request.GET['page'])

    response = {'html': '', 'page': 1, 'page_count': 1}

    if string == '':
        string = '*'

    context = {}
    if len(topics) > TOPIC_SEARCH_LIMIT:
        context['limit'] = TOPIC_SEARCH_LIMIT
        topics = topics[:TOPIC_SEARCH_LIMIT]

    results = searches.search(string, topics, min_show, max_show)
    context['matches'] = results.count()
    context['results'], response['page'], response['page_count'] = \
        searches.paginate(results, page, RESULTS_SEARCH_LIMIT)

    template = 'shownotes/topic-container.html'
    if page > 1:
        template = 'shownotes/topic-list.html'
    response['html'] = render_to_string(template, context)
    return HttpResponse(json.dumps(response),
                        content_type='application/json')
