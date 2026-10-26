from support.catalog_samples import catalog_with
from support.fakes import RecordingCatalogWriter
from support.session_samples import DOCUMENT, ENGLISH, open_document

from xlf_translator.application.catalog_writer import CatalogWriter


def test_the_fake_writer_satisfies_the_port():
    assert isinstance(RecordingCatalogWriter(), CatalogWriter)


def test_the_writer_receives_the_original_document():
    writer = RecordingCatalogWriter()
    open_document(catalog_with(3)).export_draft(writer)
    assert writer.calls == [(DOCUMENT, catalog_with(3), ENGLISH)]
