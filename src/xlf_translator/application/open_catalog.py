from xlf_translator.application.catalog_reader import CatalogReader
from xlf_translator.application.open_document import OpenDocument
from xlf_translator.application.session_repository import SessionRepository
from xlf_translator.application.session_view import SessionView
from xlf_translator.domain.catalog_refusal import CatalogRefusal
from xlf_translator.domain.translation_session import TranslationSession
from xlf_translator.domain.uploaded_document import UploadedDocument


class OpenCatalog:
    """Opens a translation session over an uploaded document, or says why it cannot."""

    def __init__(self, reader: CatalogReader, repository: SessionRepository):
        self._reader = reader
        self._repository = repository

    def execute(self, document: UploadedDocument) -> SessionView | CatalogRefusal:
        size = document.size()
        if not size.is_within_limit():
            return size.refusal()
        read = self._reader.read(document)
        if isinstance(read, CatalogRefusal):
            return read
        open_document = OpenDocument(document, TranslationSession.resumed(*read))
        self._repository.save(open_document)
        return open_document.describe()
