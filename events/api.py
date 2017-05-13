from django.shortcuts import redirect
from rest_framework import generics

from .serializers import (
    EventProposeSerializer,
    EventSerializer, BetSerializer, TransactionSerializer
)
from .models import Event, Bet, Transaction


class CreateEventView(generics.CreateAPIView):
    model = Event
    queryset = Event.objects.all()
    serializer_class = EventProposeSerializer
    # permissions = []

    def perform_create(self, serializer):
        """Force author to the current user on save"""
        instance = serializer.save(created_by=self.request.user, is_published=False)
        self.redirect_to = instance.get_relative_url()
        return instance

    def post(self, request, *args, **kwargs):
        super(CreateEventView, self).post(request, *args, **kwargs)
        return redirect(self.redirect_to)


class EventMixin(object):
    model = Event
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permissions = []

    def perform_create(self, serializer):
        """Force author to the current user on save"""
        serializer.save(created_by=self.request.user)


class EventList(EventMixin, generics.ListCreateAPIView):
    pass


class EventDetail(EventMixin, generics.RetrieveAPIView):
    pass


class BetMixin(object):
    model = Bet
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permissions = []


class BetList(BetMixin, generics.ListAPIView):
    pass


class BetDetail(BetMixin, generics.RetrieveAPIView):
    pass


class TransactionMixin(object):
    model = Transaction
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permissions = []

    def perform_create(self, serializer):
        """Force author to the current user on save"""
        serializer.save(created_by=self.request.user)


class TransactionList(TransactionMixin, generics.ListCreateAPIView):
    pass


class TransactionDetail(TransactionMixin, generics.RetrieveAPIView):
    pass
