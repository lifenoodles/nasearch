from models import Topic
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery
from haystack.utils import Highlighter
import json
import re


TOPIC_SEARCH_LIMIT = 10
RESULTS_SEARCH_LIMIT = 20


class HtmlHighlighter(Highlighter):
    def render_html(self, highlight_locations=None,
                    start_offset=None, end_offset=None):
        print highlight_locations
        highlighted_chunk = self.text_block
        for word in self.query_words:
            print word
            pattern = re.compile(word, re.IGNORECASE)
            highlighted_chunk = pattern.sub(
                '<span class="highlighted">{}</span>'.format(word),
                highlighted_chunk)
        return highlighted_chunk


def index(request):
    return render(request, 'shownotes/index.html')


def search_topics(request):
    if 'string' in request.GET \
            and 'topics' in request.GET \
            and 'page' in request.GET:
        results = []
        topic_ids = [int(t) for t in request.GET['topics'].split()]
        context = {}

        if len(topic_ids) > TOPIC_SEARCH_LIMIT:
            context['limit'] = TOPIC_SEARCH_LIMIT
            topic_ids = topic_ids[:TOPIC_SEARCH_LIMIT]

        if request.GET['string'] == '':
            if len(topic_ids) == 0:
                return render(request, 'shownotes/empty-topic.html')
            results = SearchQuerySet().filter(topic_id__in=topic_ids) \
                .order_by('-show_number').order_by('topic_name')
        else:
            query = request.GET['string']
            results = SearchQuerySet().filter(topic_id__in=topic_ids) \
                .filter(SQ(text=AutoQuery(query)) |
                        SQ(text_entry=AutoQuery(query)))

        paginator = Paginator(results, RESULTS_SEARCH_LIMIT)
        try:
            results = paginator.page(request.GET['page'])
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = []

        context['results'] = results
        if request.GET['page'] == '1':
            return render(
                request, 'shownotes/topic-container.html', context)
        else:
            return render(
                request, 'shownotes/topic-list.html', context)
    else:
        return render(request, 'shownotes/topic-container.html')


def topics(request):
    topics = Topic.objects.all()
    topics = [{'text': t.name, 'id': t.id} for t in topics]
    topics.sort(key=lambda x: x['text'])
    return HttpResponse(json.dumps(topics),
                        content_type='application/json')
