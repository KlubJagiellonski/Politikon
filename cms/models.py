from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserProfile


class Page(models.Model):
    """
    Separated page for any content
    """
    is_published = models.BooleanField(
        default=False,
        verbose_name=_('Is published'),
    )
    user_profile = models.ForeignKey(
        to=UserProfile,
        related_name='page',
        related_query_name='pages',
        verbose_name=_('Author'),
    )
    title = models.CharField(
        verbose_name=_('News title'),
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=_('Slug url'),
        unique=True
    )
    created_at = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Edition date'),
        auto_now_add=True,
    )
    content = models.TextField(
        verbose_name=_('Content'),
    )
    lang = models.CharField(
        verbose_name=_('Language'),
        max_length=2,
        default='pl'
    )

    def get_absolute_url(self):
        """
        Get this user url

        :return: user url
        :rtype: str
        """
        return reverse('cms:page', kwargs={'slug': self.slug})


class ExtraContent(models.Model):
    """
    Extra content for chosen page
    """
    user_profile = models.ForeignKey(
        to=UserProfile,
        related_name='extra_content',
        related_query_name='extra_contents',
        verbose_name=_('Author'),
    )
    # Tag code is used to place this content on page ex: {% about-us %}
    tag_code = models.SlugField(
        verbose_name=_('Tag code'),
    )
    created_at = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Edition date'),
        auto_now_add=True,
    )
    content = models.TextField(
        verbose_name=_('Content'),
    )
    lang = models.CharField(
        verbose_name=_('Language'),
        max_length=2,
        default='pl'
    )
