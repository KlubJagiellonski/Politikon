from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import UserProfile


class Page(models.Model):
    """
    Separated page for any content
    """
    is_published = models.BooleanField(default=False, verbose_name=_('is published'))
    user_profile = models.ForeignKey(
        to=UserProfile,
        related_name='page',
        related_query_name='pages',
        verbose_name=_('author'),
    )
    title = models.CharField(verbose_name=_('news title'), max_length=255)
    slug = models.SlugField(verbose_name=_('slug url'), unique=False)
    created_at = models.DateTimeField(verbose_name=_('creation date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('edition date'), auto_now_add=True)
    content = models.TextField(verbose_name=_('content'))
    lang = models.CharField(verbose_name=_('language'), max_length=2, default='pl')

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')

    def __unicode__(self):
        return self.title

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
        verbose_name=_('author')
    )
    # Tag code is used to place this content on page ex: {% about-us %}
    tag_code = models.SlugField(verbose_name=_('tag code'))
    created_at = models.DateTimeField(verbose_name=_('creation date'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('edition date'), auto_now_add=True)
    content = models.TextField(verbose_name=_('content'))
    lang = models.CharField(verbose_name=_('language'), max_length=2, default='pl')

    class Meta:
        verbose_name = _('extra content')
        verbose_name_plural = _('extra contents')


class GalleryImage(models.Model):
    name = models.CharField(_('name'), max_length=50)
    image = models.ImageField(upload_to='images')
    author = models.ForeignKey(to=UserProfile, verbose_name=_('author'))
    created_at = models.DateTimeField(verbose_name=_('creation date'), auto_now_add=True)

    class Meta:
        verbose_name = _('gallery image')
        verbose_name_plural = _('gallery images')

    def __unicode__(self):
        return self.name
