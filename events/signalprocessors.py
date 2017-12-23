from django.db import models
from haystack import signals
from celery_haystack.signals import CelerySignalProcessor

from .models import Event


class EventSignalProcessor(CelerySignalProcessor):
    """
    Extend CelerySignalProcessor used in this project to work with Event model
    """
    def setup(self):
        super(EventSignalProcessor, self).setup()
        models.signals.post_save.connect(self.handle_save, sender=Event)
        models.signals.post_delete.connect(self.handle_delete, sender=Event)

    def teardown(self):
        super(EventSignalProcessor, self).teardown()
        models.signals.post_save.disconnect(self.handle_save, sender=Event)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Event)

