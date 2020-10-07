from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
    InlinePanel
)
from wagtail.api import APIField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.search import index

from streams import blocks

class HomePageCarouselImages(Orderable):
    """A carousel with 1 to 5 images title and text"""

    page = ParentalKey("home.HomePage", related_name='carousel_images')
    title = models.CharField(max_length=40, blank=False, null=True)
    text = RichTextField()
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
        ImageChooserPanel('carousel_image')
    ]

class HomePage(RoutablePageMixin, Page):
    """Home page model"""

    template = "home/home_page.html"
    max_count = 1 # how many page of this type can be

    # django field
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content = StreamField(
        [
            ("cta", blocks.CtaBlock()),
        ],
        null=True,
        blank=True
    )

    api_fields = [
        APIField('banner_title'),
        APIField('banner_subtitle'),
        APIField('banner_image'),
        APIField('banner_cta')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('first_published_at', partial_match=True, boost=2),
    ]

    # cms panel
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
                ImageChooserPanel("banner_image"),
                PageChooserPanel("banner_cta"),
            ], heading='banner options'
        ),
        MultiFieldPanel(
            [
                InlinePanel('carousel_images', max_num=5, min_num=1, label='Image')
            ], heading='carousel'
        ),
        StreamFieldPanel("content")
    ]

    # metadata
    class Meta:
        verbose_name = "Home Page" # the name of the rtype of page that appear in cms
        verbose_name_plural = "Home Pages"

    @route(r'subscribe/$')
    def subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, *kwargs)
        return render(request, 'home/subscribe.html', context)
