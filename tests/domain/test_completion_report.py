from support.catalog_samples import catalog_with
from support.recorders import described

from xlf_translator.domain.completion_report import CompletionReport


def test_a_fully_translated_catalog_is_complete():
    assert CompletionReport(catalog_with(60, auto_filled=[30])).is_complete()


def test_untranslated_and_invalid_ordinals_are_named_together():
    report = CompletionReport(catalog_with(60, untranslated=[31, 38], invalid=[44, 52]))
    assert not report.is_complete()
    assert report.unresolved() == (31, 38, 44, 52)
    assert described(report)["completion"] == ((31, 38), (44, 52))
