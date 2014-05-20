from models import Note, Show
from django.shortcuts import render
from collections import defaultdict


def index(request):
    return render(request, 'shownotes/index.html', {'text': 'Hello'})


def search_topics(request):
    if 'string' in request.GET:
        notes = Note.get_by_topic(
            request.GET['string']).order_by('-show')
        show_map = defaultdict(list)
        for note in notes:
            show_map[note.show].append(note)
        show_notes = [(s, n) for s, n in show_map.items()]
        show_notes.sort(reverse=True,
                        key=lambda (x, _): x.id)

        context = {'show_notes': show_notes}
        return render(
            request, 'shownotes/topic-list.html', context)
    else:
        return render(request, 'shownotes/topic-list.html')


def note_details(request):
    pass
