from xml.etree.ElementTree import Element, ParseError

from xlf_translator.application.catalog_reader import CatalogReader
from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.catalog_refusal import CatalogRefusal
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.language_pair import LanguagePair
from xlf_translator.domain.translation_unit import TranslationUnit
from xlf_translator.domain.unit_identifier import UnitIdentifier
from xlf_translator.domain.uploaded_document import UploadedDocument
from xlf_translator.infrastructure.content_from_element import ContentFromElement
from xlf_translator.infrastructure.encoding_check import EncodingCheck
from xlf_translator.infrastructure.xliff_document import XliffDocument

SUPPORTED_VERSION = "1.2"


class ElementTreeCatalogReader(CatalogReader):
    """Reads an XLIFF 1.2 document with the standard library's ElementTree."""

    def read(self, document: UploadedDocument) -> tuple[Catalog, LanguagePair] | CatalogRefusal:
        content = bytes(document)
        refusal = EncodingCheck(content).refusal()
        if refusal:
            return refusal
        parsed = XliffDocument.parse(content)
        if isinstance(parsed, ParseError):
            return CatalogRefusal("well-formed XML", f"a syntax error ({parsed})")
        return self._read_document(parsed)

    def _read_document(self, xliff: XliffDocument) -> tuple[Catalog, LanguagePair] | CatalogRefusal:
        refusal = self._root_refusal(xliff)
        if refusal:
            return refusal
        files = xliff.root().findall(xliff.tag("file"))
        if len(files) != 1:
            return CatalogRefusal("exactly one <file> element", f"{len(files)}")
        languages = self._languages(files[0])
        if isinstance(languages, CatalogRefusal):
            return languages
        catalog = self._catalog(xliff, files[0])
        return catalog if isinstance(catalog, CatalogRefusal) else (catalog, languages)

    @staticmethod
    def _root_refusal(xliff: XliffDocument) -> CatalogRefusal | None:
        name = XliffDocument.local_name(xliff.root())
        if name != "xliff":
            return CatalogRefusal("an <xliff> root element", f"<{name}>")
        version = xliff.root().get("version")
        if version != SUPPORTED_VERSION:
            return CatalogRefusal(f"XLIFF version {SUPPORTED_VERSION}", f"version {version or 'undeclared'}")
        return None

    @staticmethod
    def _languages(file: Element) -> LanguagePair | CatalogRefusal:
        source, target = file.get("source-language"), file.get("target-language")
        if source is None:
            return CatalogRefusal("a source language declared on <file>", "none")
        malformed = [code for code in (source, target) if code is not None and not LanguageCode.accepts(code)]
        if malformed:
            return CatalogRefusal("a language code such as en-GB", f"'{malformed[0]}'")
        return LanguagePair(LanguageCode(source), target and LanguageCode(target))

    def _catalog(self, xliff: XliffDocument, file: Element) -> Catalog | CatalogRefusal:
        elements = list(file.iter(xliff.tag("trans-unit")))
        if not elements:
            return CatalogRefusal("at least one trans-unit", "none")
        units = [self._unit(xliff, element, ordinal) for ordinal, element in enumerate(elements, start=1)]
        refusals = [unit for unit in units if isinstance(unit, CatalogRefusal)]
        return refusals[0] if refusals else Catalog.of(units)

    def _unit(self, xliff: XliffDocument, element: Element, ordinal: int) -> TranslationUnit | CatalogRefusal:
        identifier = (element.get("id") or "").strip()
        source = element.find(xliff.tag("source"))
        if not identifier or source is None:
            return CatalogRefusal("an id and a <source> in every trans-unit", f"trans-unit {ordinal} lacking one")
        target = element.find(xliff.tag("target"))
        refusal = self._inline_refusal(identifier, source) or (target is not None and self._inline_refusal(identifier, target))
        if refusal:
            return refusal
        target_content = target if target is None else ContentFromElement(target).content()
        return TranslationUnit.parsed(UnitIdentifier(identifier), ContentFromElement(source).content(), target_content)

    @staticmethod
    def _inline_refusal(identifier: str, element: Element) -> CatalogRefusal | None:
        foreign = ContentFromElement(element).foreign_child()
        if foreign is None:
            return None
        return CatalogRefusal("only <x/> inline elements", f"<{foreign}> in trans-unit '{identifier}'")
