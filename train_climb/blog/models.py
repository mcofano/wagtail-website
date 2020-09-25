from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey, ForeignKey

from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet

from streams import blocks

class BlogAuthorsOrderable(Orderable):
    """An intermediat table that allows to select more authors for a blog post page.
    It implements a many to many relationship between blog detail page and authors."""

    page = ParentalKey('blog.BlogDetailPage', related_name='blog_authors')
    author = ForeignKey(
        'blog.BlogAuthor',
        on_delete=models.CASCADE
    )

    panel = [
        SnippetChooserPanel('author')
    ]

class BlogAuthor(models.Model):
    """Authors of the blog posts"""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='+',
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('name'),
                ImageChooserPanel('image')
            ], heading='Name and Image',
        ),
        MultiFieldPanel(
            [
                FieldPanel('website')
            ], heading='Links'
        )
    ]

    def __str__(self):
        """Representation of class"""
        return self.name

    class Meta:
        verbose_name = 'Blog Author'
        verbose_name_plural = 'Blog Authors'

register_snippet(BlogAuthor)


class BlogListingPage(RoutablePageMixin, Page):
    """Blog to list all the blog entries page"""

    template = 'blog/blog_listing_page.html'

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title"
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title')
    ]

    def get_context(self, request, *args, **kwargs):
        """adding custum stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context['posts'] = BlogDetailPage.objects.live().public() # query  set!  ->  live an public blog detail pages
        return context

    @route(r'latest/$', name= 'latest_posts')
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, *kwargs)
        context['latest_posts'] = context['posts'][:1]
        return render(request, 'blog/latest_posts.html', context)


class BlogDetailPage(Page):
    """Blog pages"""
    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title"
    )
    blog_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL
    )
    content = StreamField(
        [
            ('Title_and_text', blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("card", blocks.CardBlock()),
            ("cta", blocks.CtaBlock()),
        ],
        null=True,
        blank=False
    )

    content_panels = Page.content_panels + [
        FieldPanel('custom_title'),
        ImageChooserPanel('blog_image'),
        MultiFieldPanel(
            [
                InlinePanel('blog_authors', label="Author", min_num=1, max_num=4)
            ], heading='Authors'
        ),
        StreamFieldPanel("content")
    ]

