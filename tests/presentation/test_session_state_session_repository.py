from support.catalog_samples import catalog_with
from support.session_samples import open_document

from xlf_translator.application.session_repository import SessionRepository
from xlf_translator.presentation.session_state_session_repository import SessionStateSessionRepository


def test_the_repository_implements_the_port():
    assert isinstance(SessionStateSessionRepository({}), SessionRepository)


def test_an_open_document_survives_a_rerun():
    state = {}
    SessionStateSessionRepository(state).save(open_document(catalog_with(3)))
    assert SessionStateSessionRepository(state).load() == open_document(catalog_with(3))


def test_the_document_is_kept_apart_from_widget_state():
    state = {"target::unit.1": "typed"}
    repository = SessionStateSessionRepository(state)
    repository.save(open_document(catalog_with(3)))
    state.pop("target::unit.1")
    assert repository.load() == open_document(catalog_with(3))


def test_clearing_forgets_the_document():
    repository = SessionStateSessionRepository({})
    repository.save(open_document(catalog_with(3)))
    repository.clear()
    assert repository.load() is None
