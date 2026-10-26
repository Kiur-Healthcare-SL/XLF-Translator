"""In-memory implementations of the application ports."""

from xlf_translator.application.catalog_reader import CatalogReader
from xlf_translator.application.catalog_writer import CatalogWriter
from xlf_translator.application.session_repository import SessionRepository


class InMemoryCatalogReader(CatalogReader):
    def __init__(self, answer):
        self.answer = answer
        self.read_documents = []

    def read(self, document):
        self.read_documents.append(document)
        return self.answer


class RecordingCatalogWriter(CatalogWriter):
    def __init__(self):
        self.calls = []

    def write(self, document, catalog, language):
        self.calls.append((document, catalog, language))
        return f"{document}:{language}".encode()


class InMemorySessionRepository(SessionRepository):
    def __init__(self, open_document=None):
        self.open_document = open_document

    def load(self):
        return self.open_document

    def save(self, open_document):
        self.open_document = open_document

    def clear(self):
        self.open_document = None
