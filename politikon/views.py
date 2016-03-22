import json

from constance import config

from django.views.generic import TemplateView
from django.http import HttpResponse

from accounts.models import UserProfile
from events.models import Event


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        user = self.get_object()
        json_data = {}

        context = super(HomeView, self).get_context_data(*args, **kwargs)
        front_event = Event.objects.get_front_event()

        if front_event:
            context.update({
                'front_event': front_event,
                'front_event_bet': front_event.get_user_bet(user),
            })
            json_data['front_event'] = json.\
                dumps(front_event.get_chart_points())
        else:
            json_data['front_event'] = 'null'

        featured_events = list(Event.objects.get_featured_events()[:6])
        for i in range(len(featured_events)):
            featured_events[i].my_bet = featured_events[i].get_user_bet(user)
        popular_events = list(Event.objects.get_events('popular')[:3])
        for i in range(len(popular_events)):
            popular_events[i].my_bet = popular_events[i].get_user_bet(user)

        json_data['events'] = self.\
            makeFeaturedEventsBetfeedData(popular_events + featured_events)

        context.update({
            'featured_events': featured_events,
            'popular_events': popular_events,
            'json_data': json_data,
            'config': config,
            'best_weekly': UserProfile.objects.get_best_weekly()[:10],
            'best_monthly': UserProfile.objects.get_best_monthly()[:10],
            'best_overall': UserProfile.objects.get_best_overall()[:10]
        })
        return context

    def makeFeaturedEventsBetfeedData(self, events):
        data = []
        for ev in events:
            data.append(ev.get_chart_points())
        return json.dumps(data)


def acme_challenge(request):
    """
    Make sure your web server displays the following content at
    http://www.politikon.org.pl/.well-known/acme-challenge/lMSbr1wkgq8wCK1aSU-hMDN4xuvwsx3GQjYiwh922XI
    before continuing:

    :param request:
    :type request: HttpRequest
    :return:
    :rtype: HttpResponse
    """
    response = '44jmcY27vf0Xqc44v7-kQx0O1ANUx5OeHysmzhxe_cc.gH-uL0atBurquAoT' \
               'yPdNCmWNE4OqrHNOWrVMMu94hrU'


    return HttpResponse(response)
