from support.catalog_samples import catalog_with
from support.session_samples import repository_over

from xlf_translator.application.choose_target_language import ChooseTargetLanguage
from xlf_translator.domain.catalog_refusal import CatalogRefusal


def test_the_chosen_language_reaches_the_session():
    repository = repository_over(catalog_with(3, default="untranslated"), target=None)
    view = ChooseTargetLanguage(repository).execute("en-GB")
    assert view.target_language == "en-GB"
    assert repository.load().describe().target_language == "en-GB"


def test_a_malformed_language_is_refused():
    repository = repository_over(catalog_with(3, default="untranslated"), target=None)
    refusal = ChooseTargetLanguage(repository).execute("English")
    assert isinstance(refusal, CatalogRefusal)
    assert repository.load().describe().needs_target_language()
