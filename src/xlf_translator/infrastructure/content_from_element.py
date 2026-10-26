from xml.etree.ElementTree import Element

from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder import Placeholder
from xlf_translator.domain.placeholder_attributes import PlaceholderAttributes
from xlf_translator.domain.placeholder_name import PlaceholderName
from xlf_translator.domain.text_run import TextRun
from xlf_translator.infrastructure.xliff_document import XliffDocument

PLACEHOLDER = "x"


class ContentFromElement:
    """Reads a `<source>` or `<target>` into content: its text and its `<x/>` children."""

    def __init__(self, element: Element):
        self._element = element

    def foreign_child(self) -> str | None:
        """The first child that is not an `<x/>` placeholder, which content cannot hold."""
        names = [XliffDocument.local_name(child) for child in self._element]
        foreign = [name for name in names if name != PLACEHOLDER]
        return foreign[0] if foreign else None

    def content(self) -> Content:
        items = [TextRun(self._element.text or "")]
        for child in self._element:
            items += [ContentFromElement._placeholder(child), TextRun(child.tail or "")]
        return Content(items)

    @staticmethod
    def _placeholder(child: Element) -> Placeholder:
        attributes = PlaceholderAttributes(tuple(child.attrib.items()))
        return Placeholder(PlaceholderName(child.get("id", "")), attributes)
