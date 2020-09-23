""" Flexible page """

from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

class Flex(Page):
    """Flexible page class"""
    template = 'flex/flex_page.html'

    # todo
    # add a stream field
    # content = Streamfield()

    subtitle = models.CharField(max_length=100,
                                null=True,
                                blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle')
    ]

    class Meta:
        verbose_name = 'Flex Page'
        verbose_name_plural = 'Fles Pages'
