from support.catalog_samples import catalog_with
from support.session_samples import repository_over

from xlf_translator.application.enter_target import EnterTarget


def entered(target, **states):
    repository = repository_over(catalog_with(3, **states))
    return EnterTarget(repository).execute("unit.1", target), repository


def test_a_matching_target_translates_the_unit():
    view, _ = entered("{2}palabra{1}", untranslated=[1])
    assert view.state == "translated"


def test_a_whitespace_only_target_is_untranslated():
    view, repository = entered("   ")
    assert view.state == "untranslated"
    assert repository.load().describe().untranslated == (1,)


def test_a_mismatch_returns_the_placeholder_difference():
    view, _ = entered("{1}palabra", untranslated=[1])
    assert view.state == "invalid"
    assert view.problems == ("{2} (</b>) is missing",)


def test_clearing_an_invalid_target_makes_it_untranslated():
    view, _ = entered("", invalid=[1])
    assert view.state == "untranslated"
