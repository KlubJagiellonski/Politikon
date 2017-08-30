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

    def get_object(self, queryset=None):
        """
        Get page for specified language
        :param queryset: current queryset
        :type queryset: QuerySet
        :return: instance of Page
        :rtype: Page
        """
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(lang=self.request.LANGUAGE_CODE)
        return super(PageDetailView, self).get_object(queryset)
