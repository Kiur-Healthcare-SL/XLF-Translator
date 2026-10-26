"""Use cases wired to the real XLIFF adapters and an in-memory session."""

from support.fakes import InMemorySessionRepository
from support.fixture_documents import fixture

from xlf_translator.infrastructure.element_tree_catalog_reader import ElementTreeCatalogReader
from xlf_translator.infrastructure.element_tree_catalog_writer import ElementTreeCatalogWriter
from xlf_translator.presentation.use_cases import UseCases


def wired():
    return UseCases.wired(InMemorySessionRepository(), ElementTreeCatalogReader(), ElementTreeCatalogWriter())


def opened(name):
    use_cases = wired()
    return use_cases, use_cases.open_catalog.execute(fixture(name))
