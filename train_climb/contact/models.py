from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldRowPanel, FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class ContactPage(AbstractEmailForm):
    """Contact page Form Page"""
    template = 'contact/contact_page.html'

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = [
        FieldPanel('title'),
        FieldPanel('intro'),
        InlinePanel('form_fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
                FieldRowPanel([
                    FieldPanel('from_address', classname="col6"),
                    FieldPanel('to_address', classname='col6'),
                ]),
                FieldPanel('subject')
            ], heading='Email Settings'),
    ]

