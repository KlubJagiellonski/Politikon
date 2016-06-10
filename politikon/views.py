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

        context = super(HomeView, self).get_context_data(*args, **kwargs)
        home_events = Event.objects.get_featured_events().order_by('?')[:7]
        front_event = home_events[0]

        if front_event:
            context.update({
                'front_event': front_event,
                'front_event_bet': front_event.get_user_bet(user),
            })

        featured_events = home_events[1:7]
        for i in range(len(featured_events)):
            featured_events[i].my_bet = featured_events[i].get_user_bet(user)
        last_minute_events = list(Event.objects.get_events('last-minute')[:3])
        for i in range(len(last_minute_events)):
            last_minute_events[i].my_bet = last_minute_events[i].get_user_bet(user)

        context.update({
            'featured_events': featured_events,
            'last_minute_events': last_minute_events,
            'config': config,
            'best_weekly': UserProfile.objects.get_best_weekly()[:10],
            'best_monthly': UserProfile.objects.get_best_monthly()[:10],
            'best_overall': UserProfile.objects.get_best_overall()[:10]
        })
        return context


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
    response = 'sJN3Ermg6w3afMwhPJ2PPlatJ9RXlWFDTeDnHzccpdU.Y7pUq0Nm4uLkCi6OkzsKAJFImCjQAd1XDl-VBHNwvSE'

    return HttpResponse(response)
