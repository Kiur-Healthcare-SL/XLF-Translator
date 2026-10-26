from support.content_samples import BOLD_PHRASE, CLOSE_BOLD, OPEN_BOLD, content

from xlf_translator.domain.content import Content
from xlf_translator.domain.source_content import SourceContent

SOURCE = SourceContent(BOLD_PHRASE)


def test_a_source_masks_itself():
    assert SOURCE.masked() == "{1}limited functionality{2}"


def test_a_source_masks_and_unmasks_a_target():
    target = content(CLOSE_BOLD, "x", OPEN_BOLD)
    assert SOURCE.unmask(SOURCE.mask(target)) == target


def test_a_source_compares_a_masked_target():
    assert not SOURCE.compare("{1}").matches()


def test_a_whitespace_source_is_blank():
    assert SourceContent(Content.of_text("  ")).is_blank()
