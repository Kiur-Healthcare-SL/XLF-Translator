"""The D14 fixtures as uploaded documents, read and written by the real adapters."""

from pathlib import Path

from xlf_translator.domain.uploaded_document import UploadedDocument
from xlf_translator.infrastructure.element_tree_catalog_reader import ElementTreeCatalogReader

FIXTURES = Path(__file__).parents[1] / "fixtures"
FRESH = "messages.xlf"
PARTIAL = "messages.en-GB.xlf"
COMPLETED = "messages.fr.xlf"
ALL = (FRESH, PARTIAL, COMPLETED)


def fixture(name):
    return UploadedDocument(name, (FIXTURES / name).read_bytes())


def read(name):
    return ElementTreeCatalogReader().read(fixture(name))


def document(text, name="sample.xlf"):
    return UploadedDocument(name, text.encode("utf-8") if isinstance(text, str) else text)


def xliff(units, file_attributes='source-language="es"', version="1.2"):
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<xliff version="{version}" xmlns="urn:oasis:names:tc:xliff:document:1.2">\n'
        f"  <file {file_attributes} datatype=\"plaintext\">\n    <body>\n{units}\n    </body>\n  </file>\n</xliff>\n"
    )


def trans_unit(identifier, source, target=None):
    target_element = "" if target is None else f"\n        <target>{target}</target>"
    return f'      <trans-unit id="{identifier}">\n        <source>{source}</source>{target_element}\n      </trans-unit>'
