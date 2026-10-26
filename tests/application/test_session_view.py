from xlf_translator.application.session_view import SessionView


def view(target_language="en-GB", untranslated=(), invalid=()):
    return SessionView("messages.xlf", 1, 60, "es", target_language, "partial", (30,), untranslated, invalid)


def test_a_view_without_target_language_needs_one():
    assert view(None).needs_target_language()
    assert not view().needs_target_language()


def test_unresolved_ordinals_merge_in_order():
    incomplete = view(untranslated=(31, 38), invalid=(44, 52, 2))
    assert incomplete.unresolved() == (2, 31, 38, 44, 52)
    assert not incomplete.is_complete()
    assert view().is_complete()
