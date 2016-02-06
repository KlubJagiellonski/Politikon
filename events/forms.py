# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from .models import Event

class EventForm(forms.ModelForm):
    solve_event = forms.CharField(label="Rozstrzygnij event. TAK / NIE / \
                                  ANULUJ", required=False)

    def clean_solve_event(self):
        solve_event = self.cleaned_data['solve_event']
        if solve_event not in ('', 'TAK', 'NIE', 'ANULUJ'):
            raise ValidationError(u'Błędne rozstrzygnięcie wydarzenia. \
                                  Wpisz jedno z: TAK / NIE / ANULUJ')
        return solve_event

    def __init__(self, *args, **kwargs):
        self.action = None
        super(EventForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Event
        exclude = ()
