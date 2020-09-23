""" Flexible page """

from django.db import models
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from streams import blocks

class Flex(Page):
    """Flexible page class"""
    template = 'flex/flex_page.html'

    # add a stream field
    content = StreamField(
        [
            ('Title_and_text', blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("card", blocks.CardBlock())
        ],
        null=True,
        blank=True
    )

    subtitle = models.CharField(max_length=100,
                                null=True,
                                blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        StreamFieldPanel("content")
    ]

    class Meta:
        verbose_name = 'Flex Page'
        verbose_name_plural = 'Fles Pages'
