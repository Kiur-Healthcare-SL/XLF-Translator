from xml.etree.ElementTree import register_namespace, tostring

from xlf_translator.application.catalog_writer import CatalogWriter
from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.uploaded_document import UploadedDocument
from xlf_translator.infrastructure.encoding_check import BYTE_ORDER_MARK
from xlf_translator.infrastructure.target_placement import TargetPlacement
from xlf_translator.infrastructure.xliff_document import XliffDocument

DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>\n'
# ElementTree closes empty elements with " />"; Angular writes "/>". Text and
# attribute values escape ">", so the sequence only ever ends an empty tag.
EMPTY_ELEMENT_END = " />"
ANGULAR_EMPTY_ELEMENT_END = "/>"


class ElementTreeCatalogWriter(CatalogWriter):
    """Writes a catalog's targets into the re-parsed original document (design D10).

    The document is one the reader accepted, so it parses.
    """

    def write(self, document: UploadedDocument, catalog: Catalog, language: LanguageCode) -> bytes:
        xliff = XliffDocument.parse(bytes(document).removeprefix(BYTE_ORDER_MARK))
        register_namespace("", xliff.namespace())
        file = xliff.root().find(xliff.tag("file"))
        file.set("target-language", str(language))
        elements = {element.get("id").strip(): element for element in file.iter(xliff.tag("trans-unit"))}
        catalog.write_into(TargetPlacement(xliff, elements))
        serialised = tostring(xliff.root(), encoding="unicode").replace(EMPTY_ELEMENT_END, ANGULAR_EMPTY_ELEMENT_END)
        return (DECLARATION + serialised + "\n").encode("utf-8")
