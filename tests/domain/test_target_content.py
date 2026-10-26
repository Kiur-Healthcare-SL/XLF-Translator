from support.content_samples import BOLD_PHRASE

from xlf_translator.domain.source_content import SourceContent
from xlf_translator.domain.target_content import TargetContent


def test_empty_and_whitespace_targets_are_blank():
    assert TargetContent("").is_blank()
    assert TargetContent("   ").is_blank()
    assert not TargetContent(" x ").is_blank()


def test_a_target_compares_and_unmasks_against_its_source():
    source = SourceContent(BOLD_PHRASE)
    target = TargetContent("{1}limited functionality{2}")
    assert target.compared_with(source).matches()
    assert target.unmasked_by(source) == BOLD_PHRASE


def test_a_target_renders_as_its_masked_text():
    assert str(TargetContent("{2}x{1}")) == "{2}x{1}"
