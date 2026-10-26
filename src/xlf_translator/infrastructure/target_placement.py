from xml.etree.ElementTree import Element

from xlf_translator.domain.content import Content
from xlf_translator.domain.translation_unit import TranslationUnit
from xlf_translator.domain.unit_identifier import UnitIdentifier
from xlf_translator.infrastructure.content_from_element import ContentFromElement
from xlf_translator.infrastructure.content_into_element import ContentIntoElement
from xlf_translator.infrastructure.xliff_document import XliffDocument


class TargetPlacement:
    """Told each unit of a catalog, edits the matching trans-unit of the parsed original (design D10).

    A unit whose original target parses to the same unit is left alone; any
    other unit gets a fresh target right after its source, or loses its target
    when it has become untranslated.
    """

    def __init__(self, xliff: XliffDocument, elements: dict[str, Element]):
        self._xliff = xliff
        self._elements = elements

    def unit(self, identifier: str, target: Content | None, unit: TranslationUnit) -> None:
        element = self._elements[identifier]
        original = element.find(self._xliff.tag("target"))
        if original is not None and self._parsed(identifier, element, original) == unit:
            return
        if original is not None:
            element.remove(original)
        if target is not None:
            self._insert(element, target)

    def _parsed(self, identifier: str, element: Element, original: Element) -> TranslationUnit:
        source = ContentFromElement(element.find(self._xliff.tag("source"))).content()
        return TranslationUnit.parsed(UnitIdentifier(identifier), source, ContentFromElement(original).content())

    def _insert(self, element: Element, target: Content) -> None:
        source = element.find(self._xliff.tag("source"))
        written = Element(self._xliff.tag("target"))
        target.write_into(ContentIntoElement(written, self._xliff.tag("x")))
        written.tail = source.tail
        element.insert(list(element).index(source) + 1, written)
