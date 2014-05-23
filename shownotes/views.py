from models import Note, UrlEntry, TextEntry, Topic
from django.shortcuts import render
from collections import defaultdict
from django.http import HttpResponse
from haystack.query import SearchQuerySet, SQ
from haystack.inputs import AutoQuery, Exact
from haystack.utils import Highlighter
import json
import re


TOPIC_SEARCH_LIMIT = 2
RESULTS_SEARCH_LIMIT = 5


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
    if 'string' in request.GET and 'topics' in request.GET:
        results = []
        topic_ids = [int(t) for t in request.GET['topics'].split()]
        context = {}

        if len(topic_ids) > TOPIC_SEARCH_LIMIT:
            context['limit'] = TOPIC_SEARCH_LIMIT
            topic_ids = topic_ids[:TOPIC_SEARCH_LIMIT]

        if request.GET['string'] == '':
            if len(topic_ids) == 0:
                return render(request, 'shownotes/empty-topic.html')
            results = SearchQuerySet().filter(topic_id__in=topic_ids)
        else:
            query = request.GET['string']
            results = SearchQuerySet().filter(topic_id__in=topic_ids) \
                .filter(SQ(text=AutoQuery(query)) |
                        SQ(note_title=AutoQuery(query)))

        if results.count() > RESULTS_SEARCH_LIMIT:
            context['results_limit'] = RESULTS_SEARCH_LIMIT

        results.load_all()

        # map entries to notes
        note_map = defaultdict(list)
        notes = set([x.object.note for x in results])
        for note in notes:
            url_entries = UrlEntry.get_by_note(note)
            for url in url_entries:
                note_map[note].append(url.link())
        for result in results:
            note_map[result.object.note].append(
                result.object.text_html())

        # map notes to shows
        show_map = defaultdict(list)
        for note in notes:
            show_map[note.show].append(note)

        # build tuples for templating
        show_notes = []
        for s, ns in show_map.items():
            note_entries = [(n, note_map[n]) for n in ns]
            show_notes.append((s, note_entries))

        show_notes.sort(reverse=True,
                        key=lambda (x, _): x.id)

        context['show_notes'] = show_notes
        return render(
            request, 'shownotes/topic-list.html', context)
    else:
        return render(request, 'shownotes/topic-list.html')


def topics(request):
    response = {}
    topics = Topic.objects.all()
    topics = [{'text': t.name, 'id': t.id} for t in topics]
    topics.sort(key=lambda x: x['text'])
    return HttpResponse(json.dumps(topics),
                        content_type='application/json')
