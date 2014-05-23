from models import Note, UrlEntry, TextEntry, Topic
from django.shortcuts import render
from collections import defaultdict
from django.http import HttpResponse
import json


TOPIC_SEARCH_LIMIT = 2


def index(request):
    return render(request, 'shownotes/index.html')


def search_topics(request):
    if 'string' in request.GET and 'topics' in request.GET:
        topic_ids = [int(t) for t in request.GET['topics'].split()]
        topics = Topic.get_by_id(*topic_ids).order_by('name')

        notes = []
        for topic in topics:
            notes += (Note.get_by_topic(topic)).order_by('-show')

        if len(notes) == 0:
            return render(request, 'shownotes/empty-topic.html')

        context = {}
        if len(notes) > TOPIC_SEARCH_LIMIT:
            context['limit'] = TOPIC_SEARCH_LIMIT

        # map entries to notes
        note_map = defaultdict(list)
        for note in notes:
            url_entries = UrlEntry.get_by_note(note)
            for url in url_entries:
                note_map[note].append(url.link())
            text_entries = TextEntry.get_by_note(note)
            for text in text_entries:
                note_map[note].append(text.text_web())

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
