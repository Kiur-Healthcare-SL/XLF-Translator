from xml.etree.ElementTree import Element, fromstring, tostring

from support.content_samples import BOLD_PHRASE, content

from xlf_translator.infrastructure.content_from_element import ContentFromElement
from xlf_translator.infrastructure.content_into_element import ContentIntoElement


def written(subject):
    element = Element("target")
    subject.write_into(ContentIntoElement(element, "x"))
    return element


def test_content_is_written_as_text_and_placeholders():
    element = written(content("Modo ", *BOLD_PHRASE, " activo"))
    assert tostring(element, encoding="unicode") == (
        '<target>Modo <x id="START_BOLD_TEXT" ctype="x-b" equiv-text="&lt;b&gt;" />limited functionality'
        '<x id="CLOSE_BOLD_TEXT" ctype="x-b" equiv-text="&lt;/b&gt;" /> activo</target>'
    )


def test_written_content_reads_back_equal():
    element = fromstring(tostring(written(BOLD_PHRASE)))
    assert ContentFromElement(element).content() == BOLD_PHRASE
