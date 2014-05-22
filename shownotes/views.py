from models import Note, UrlEntry, TextEntry
from django.shortcuts import render
from collections import defaultdict
from django.http import HttpResponse
import json


def index(request):
    return render(request, 'shownotes/index.html')


def search_topics(request):
    if 'string' in request.GET:
        notes = Note.get_by_topic(
            request.GET['string']).order_by('-show')

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

        context = {'show_notes': show_notes}
        return render(
            request, 'shownotes/topic-list.html', context)
    else:
        return render(request, 'shownotes/topic-list.html')


def topics(request):
    response = {}
    topics = Note.objects.values('topic').distinct()
    topics = [{'text': t['topic'].strip(), 'id': i}
              for t, i in zip(topics, range(len(topics)))]
    topics.sort(key=lambda x: x['text'])
    return HttpResponse(json.dumps(topics),
                        content_type='application/json')
