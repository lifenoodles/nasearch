from haystack import indexes
from shownotes.models import TextEntry, Note, UrlEntry


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    text_entry = indexes.CharField(indexed=True)
    url_entries = indexes.MultiValueField(indexed=False)
    topic_id = indexes.IntegerField(model_attr='topic__id')
    topic_name = indexes.CharField(model_attr='topic__name')
    show_number = indexes.IntegerField(model_attr='show_id')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_text_entry(self, obj):
        return ''.join(
            [t.text for t in TextEntry.objects.filter(note=obj)])

    def prepare_url_entries(self, obj):
        return [t.url for t in UrlEntry.objects.filter(note=obj)]
