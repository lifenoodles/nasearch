from models import Note, UrlEntry, TextEntry
from django.shortcuts import render
from collections import defaultdict


def index(request):
    return render(request, 'shownotes/index.html')


def search_topics(request):
    if 'string' in request.GET:
        notes = Note.get_by_topic(
            request.GET['string']).order_by('-show')
        print notes

        # map entries to notes
        note_map = defaultdict(list)
        for note in notes:
            url_entries = UrlEntry.get_by_note(note)
            for url in url_entries:
                note_map[note].append(url.link())
            text_entries = TextEntry.get_by_note(note)
            for text in text_entries:
                note_map[note].append(text.text_web())
            print note, url_entries, text_entries

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


def note_entries(request):
    pass
