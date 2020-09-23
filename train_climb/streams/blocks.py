""" Stream fields """
from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
    """ Title and text widget """

    title = blocks.CharBlock(required=True, help_text="Add your Title")
    text = blocks.CharBlock(required=True, help_text="Add your Text")

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"

class RichTextBlock(blocks.RichTextBlock):
    """Title and text with all rich text capabilities"""

    class Meta:
        template = 'streams/richtext_block.html'
        icon = 'doc-full',
        label = 'Full RichText'

class SimpleRichTextBlock(blocks.RichTextBlock):
    """Title and text with some rich text capabilities"""

    def __init__(self, required=True, help_text=None, editor='default', features=None, validators=(), **kwargs):
        super().__init__(**kwargs)
        self.features = [
            'bold',
            'italic',
            'link'
        ]

    class Meta:
        template = 'streams/richtext_block.html'
        icon = '',
        label = 'Simple RichText'


class CardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)."""

    title = blocks.CharBlock(required=True, help_text="Add your title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", blocks.TextBlock(required=True, max_length=200)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(required=False,
                        help_text="If the button page above is selected, that will be used first.",  # noqa
                    ),
                ),
            ]
        )
    )


    class Meta:  # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "cards"