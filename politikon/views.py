from django.views.generic import TemplateView

from accounts.models import UserProfile
from events.models import Event
from events.views import create_bets_dict
from constance import config
import json


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        front_event = Event.objects.get_front_event()
        featured_events = list(Event.objects.get_featured_events())
        latest_events = list(Event.objects.get_events('latest'))

        json_data = {
                'events' : self.makeFeaturedEventsBetfeedData(latest_events+featured_events),
                'front_event' : json.dumps(front_event.get_chart_points())
                }


        user = self.get_object()
        context.update({
            'front_event' : front_event,
            'featured_events': featured_events,
            'latest_events': latest_events,
            'bets': create_bets_dict(user, [front_event]+featured_events+latest_events),
            'json_data' : json_data,
            'config' : config,
            'users': UserProfile.objects.filter(is_active=True, is_deleted=False)[:30],
        })
        return context

    def makeFeaturedEventsBetfeedData(self,events):
        data = []
        for ev in events:
            data.append(ev.get_chart_points())
        return json.dumps(data)

