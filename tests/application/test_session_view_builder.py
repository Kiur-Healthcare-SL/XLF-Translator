from support.catalog_samples import catalog_with
from support.session_samples import open_document

from xlf_translator.application.session_view import SessionView


def test_a_session_describes_itself_into_a_view():
    view = open_document(catalog_with(60, auto_filled=[30], untranslated=[31])).describe()
    assert view == SessionView("messages.xlf", 31, 60, "es", "en-GB", "partial", (30,), (31,), ())
