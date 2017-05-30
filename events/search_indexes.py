from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from events.models import Event


class EventIndex(CelerySearchIndex, indexes.ModelSearchIndex, indexes.Indexable):
    tags = indexes.MultiValueField()

    class Meta:
        model = Event

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]
