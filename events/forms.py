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
