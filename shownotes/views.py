from models import Note
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'shownotes/index.html', {'text': 'Hello'})


def search_topics(request):
    if 'string' in request.GET:
        string = request.GET['string']
        notes = Note.get_by_topic(string)
        titles = [note.title for note in notes]
        context = {'titles': titles}
        return render(
            request, 'shownotes/topic-list.html', context)
    else:
        return render(request, 'shownotes/topic-list.html')
