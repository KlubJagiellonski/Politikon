from django.views import generic

from .models import Page, ExtraContent


class IndexView(generic.ListView):
    """
    List of pages
    """
    model = Page


class PageDetailView(generic.DetailView):
    """
    The page
    """
    model = Page
