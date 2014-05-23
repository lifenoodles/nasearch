from haystack import indexes
from shownotes.models import TextEntry


class TextEntryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    note_title = indexes.CharField(model_attr='note__title')
    topic_id = indexes.IntegerField(model_attr='note__topic__id')

    def get_model(self):
        return TextEntry

    def index_queryset(self, using=None):
        return self.get_model().objects.all() \
            .select_related('note').select_related('topic')
