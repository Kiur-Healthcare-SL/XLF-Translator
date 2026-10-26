from support.catalog_samples import catalog_with
from support.fakes import InMemorySessionRepository
from support.session_samples import open_document

from xlf_translator.application.session_repository import SessionRepository


def test_the_fake_repository_satisfies_the_port():
    repository = InMemorySessionRepository()
    assert isinstance(repository, SessionRepository)
    assert repository.load() is None
    repository.save(open_document(catalog_with(1)))
    assert repository.load() == open_document(catalog_with(1))
    repository.clear()
    assert repository.load() is None
