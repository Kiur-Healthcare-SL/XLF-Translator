from support.catalog_samples import catalog_with
from support.fakes import InMemoryCatalogReader, InMemorySessionRepository

from xlf_translator.application.open_catalog import OpenCatalog
from xlf_translator.domain.catalog_refusal import CatalogRefusal
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.language_pair import LanguagePair
from xlf_translator.domain.uploaded_document import UploadedDocument

FRESH = (catalog_with(60, default="untranslated", auto_filled=[30]), LanguagePair(LanguageCode("es")))
DECLARED = (catalog_with(60, untranslated=[31]), LanguagePair(LanguageCode("es"), LanguageCode("en-GB")))


def opened(answer, content=b"<xliff/>"):
    reader = InMemoryCatalogReader(answer)
    repository = InMemorySessionRepository()
    result = OpenCatalog(reader, repository).execute(UploadedDocument("messages.xlf", content))
    return result, reader, repository


def test_an_oversized_document_is_refused_before_the_reader_is_called():
    result, reader, repository = opened(FRESH, b" " * 4_194_305)
    assert "4,194,305 bytes" in str(result)
    assert reader.read_documents == []
    assert repository.load() is None


def test_a_document_at_the_limit_opens():
    result, _, repository = opened(FRESH, b" " * 4_194_304)
    assert result.total == 60
    assert repository.load() is not None


def test_a_refused_document_leaves_no_session():
    result, _, repository = opened(CatalogRefusal("XLIFF version 1.2", "version 2.0"))
    assert result == CatalogRefusal("XLIFF version 1.2", "version 2.0")
    assert repository.load() is None


def test_opening_reports_auto_filled_ordinals():
    result, _, _ = opened(FRESH)
    assert result.auto_filled == (30,)
    assert result.classification == "fresh"


def test_a_fresh_catalog_requires_a_target_language():
    result, _, _ = opened(FRESH)
    assert result.needs_target_language()


def test_a_catalog_declaring_a_target_language_adopts_it_without_asking():
    result, _, _ = opened(DECLARED)
    assert not result.needs_target_language()
    assert result.target_language == "en-GB"
    assert result.ordinal == 31
