from support.content_samples import BOLD_PHRASE
from support.session_samples import repository_over

from xlf_translator.application.copy_source_into_target import CopySourceIntoTarget
from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.content import Content
from xlf_translator.domain.translation_unit import TranslationUnit
from xlf_translator.domain.unit_identifier import UnitIdentifier


def copied(source):
    unit = TranslationUnit.parsed(UnitIdentifier("unit.1"), source, None)
    return CopySourceIntoTarget(repository_over(Catalog([unit]))).execute()


def test_tokens_arrive_in_the_target():
    view = copied(BOLD_PHRASE)
    assert view.target == "{1}limited functionality{2}"
    assert view.state == "translated"


def test_leading_non_breaking_spaces_arrive_in_the_target():
    assert copied(Content.of_text("  Volver")).target.startswith("  ")


def test_escaped_markup_arrives_in_the_target():
    assert copied(Content.of_text("<p><b>Consejo</b></p>")).target == "<p><b>Consejo</b></p>"
