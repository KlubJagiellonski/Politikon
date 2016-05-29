# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Event


class EventForm(forms.ModelForm):
    short_title = forms.CharField(label="Tytuł promocyjny", max_length=74, help_text='maksymalnie 74 znaki')
    solve_event = forms.CharField(label="Rozstrzygnij event. TAK / NIE / ANULUJ", required=False)

    class Meta:
        model = Event
        exclude = ()

    def clean_solve_event(self):
        solve_event = self.cleaned_data['solve_event']
        if solve_event not in ('', 'TAK', 'NIE', 'ANULUJ'):
            raise ValidationError(u'Błędne rozstrzygnięcie wydarzenia. Wpisz jedno ' +
                                  'z: TAK / NIE / ANULUJ')
        return solve_event

    def __init__(self, *args, **kwargs):
        self.action = None
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['estimated_end_date'].initial = timezone.now() + relativedelta(months=1)
