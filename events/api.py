from rest_framework import generics

from .serializers import EventSerializer, BetSerializer, TransactionSerializer
from .models import Event, Bet, Transaction


class EventList(generics.ListCreateAPIView):
    model = Event
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetail(generics.RetrieveAPIView):
    model = Event
    queryset = Event.objects.all()
    serializer_class = EventSerializer
