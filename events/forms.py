# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from django import forms
from django.utils import timezone

from .models import Event


class EventForm(forms.ModelForm):
    short_title = forms.CharField(label="Tytuł promocyjny", max_length=74, help_text='maksymalnie 74 znaki')

    class Meta:
        model = Event
        exclude = ()

    def __init__(self, *args, **kwargs):
        self.action = None
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['estimated_end_date'].initial = timezone.now() + relativedelta(months=1)


class EventCreateForm(forms.ModelForm):
    """
    Adding new event by politikon users form
    """
    def save(self, commit=True):
        """
        Save event form to object
        :param commit: If True, then the changes to ``instance`` will be saved to the database.
        :type commit: bool
        :return: new event instance
        :rtype: Event
        """
        self.instance.created_by = self.instance.logged_user
        return super(EventCreateForm, self).save(commit)

    class Meta:
        model = Event
        fields = ('title', 'small_image', 'big_image', 'description', 'estimated_end_date')
