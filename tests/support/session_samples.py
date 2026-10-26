"""Open documents over sample catalogs, for application tests."""

from support.fakes import InMemorySessionRepository

from xlf_translator.application.open_document import OpenDocument
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.language_pair import LanguagePair
from xlf_translator.domain.translation_session import TranslationSession
from xlf_translator.domain.uploaded_document import UploadedDocument

DOCUMENT = UploadedDocument("messages.xlf", b"<xliff/>")
SPANISH = LanguageCode("es")
ENGLISH = LanguageCode("en-GB")


def open_document(catalog, target=ENGLISH):
    return OpenDocument(DOCUMENT, TranslationSession.resumed(catalog, LanguagePair(SPANISH, target)))


def repository_over(catalog, target=ENGLISH):
    return InMemorySessionRepository(open_document(catalog, target))
