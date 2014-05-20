from models import Note, Show
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'shownotes/index.html', {'text': 'Hello'})


def search_topics(request):
    if 'string' in request.GET:
        string = request.GET['string']
        notes = Note.get_by_topic(string).order_by('-show')
        shows = notes.values('show').distinct()
        show_ids = [s['show'] for s in shows]
        shows = Show.objects.in_bulk(show_ids)
        shows = sorted(shows.values(),
                       reverse=True,
                       key=lambda x: x.id)
        show_map = {}
        for show in shows:
            show_map[show] = []
        for note in notes:
            show_map[note.show].append(note)
        print show_map

        context = {'show_map': show_map, 'shows': shows}
        return render(
            request, 'shownotes/topic-list.html', context)
    else:
        return render(request, 'shownotes/topic-list.html')
