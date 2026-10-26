from support.catalog_samples import catalog_with
from support.fakes import InMemoryCatalogReader
from support.session_samples import DOCUMENT

from xlf_translator.application.catalog_reader import CatalogReader


def test_the_fake_reader_satisfies_the_port():
    reader = InMemoryCatalogReader(catalog_with(1))
    assert isinstance(reader, CatalogReader)
    assert reader.read(DOCUMENT) == catalog_with(1)
    assert reader.read_documents == [DOCUMENT]
