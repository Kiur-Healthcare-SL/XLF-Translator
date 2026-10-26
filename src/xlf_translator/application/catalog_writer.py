from abc import ABC, abstractmethod

from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.uploaded_document import UploadedDocument


class CatalogWriter(ABC):
    """Port: writes a catalog's targets into the original document (design D3, D10)."""

    @abstractmethod
    def write(self, document: UploadedDocument, catalog: Catalog, language: LanguageCode) -> bytes:
        """Answer the bytes of the original document carrying the catalog's targets."""
