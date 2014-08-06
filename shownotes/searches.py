from shownotes.models import Topic


def topics():
    return [{'text': t.name, 'id': t.id} for t in Topic.objects.all()]
