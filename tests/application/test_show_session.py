from support.catalog_samples import catalog_with
from support.fakes import InMemorySessionRepository
from support.session_samples import repository_over

from xlf_translator.application.show_session import ShowSession


def test_no_session_is_open_before_an_upload():
    assert not ShowSession(InMemorySessionRepository()).is_open()


def test_the_open_session_and_its_current_unit_are_described():
    show = ShowSession(repository_over(catalog_with(60, untranslated=[31])))
    assert show.is_open()
    assert show.session().ordinal == 31
    assert show.current_unit().identifier == "unit.31"
