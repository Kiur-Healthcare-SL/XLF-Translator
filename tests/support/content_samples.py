"""Content built the way the reader builds it, shared by domain tests."""

from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder import Placeholder
from xlf_translator.domain.placeholder_attributes import PlaceholderAttributes
from xlf_translator.domain.placeholder_name import PlaceholderName
from xlf_translator.domain.text_run import TextRun


def placeholder(name, equivalent_text):
    attributes = (("id", name), ("ctype", "x-b"), ("equiv-text", equivalent_text))
    return Placeholder(PlaceholderName(name), PlaceholderAttributes(attributes))


OPEN_BOLD = placeholder("START_BOLD_TEXT", "<b>")
CLOSE_BOLD = placeholder("CLOSE_BOLD_TEXT", "</b>")
BOLD_PHRASE = Content([OPEN_BOLD, TextRun("limited functionality"), CLOSE_BOLD])


def content(*items):
    return Content(TextRun(item) if isinstance(item, str) else item for item in items)
