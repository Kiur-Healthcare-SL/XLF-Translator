from abc import ABC, abstractmethod

from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.catalog_refusal import CatalogRefusal
from xlf_translator.domain.language_pair import LanguagePair
from xlf_translator.domain.uploaded_document import UploadedDocument


class CatalogReader(ABC):
    """Port: reads an uploaded document into a catalog and its languages, or refuses it."""

    @abstractmethod
    def read(self, document: UploadedDocument) -> tuple[Catalog, LanguagePair] | CatalogRefusal:
        """Answer the catalog and declared languages, or why the document was refused."""
