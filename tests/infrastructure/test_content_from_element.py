from xml.etree.ElementTree import fromstring

from support.content_samples import BOLD_PHRASE

from xlf_translator.domain.content import Content
from xlf_translator.infrastructure.content_from_element import ContentFromElement

BOLD_SOURCE = (
    '<source><x id="START_BOLD_TEXT" ctype="x-b" equiv-text="&lt;b&gt;"/>limited functionality'
    '<x id="CLOSE_BOLD_TEXT" ctype="x-b" equiv-text="&lt;/b&gt;"/></source>'
)


def test_placeholders_and_text_are_read_in_order():
    assert ContentFromElement(fromstring(BOLD_SOURCE)).content() == BOLD_PHRASE


def test_escaped_markup_is_text():
    element = fromstring("<source>&lt;p&gt;Tip&lt;/p&gt;</source>")
    assert ContentFromElement(element).content() == Content.of_text("<p>Tip</p>")


def test_whitespace_is_kept():
    element = fromstring("<source>  Volver </source>")
    assert ContentFromElement(element).content() == Content.of_text("  Volver ")


def test_a_foreign_inline_element_is_named():
    assert ContentFromElement(fromstring("<source>a<g id='1'>b</g></source>")).foreign_child() == "g"
    assert ContentFromElement(fromstring(BOLD_SOURCE)).foreign_child() is None
