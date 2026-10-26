from support.catalog_samples import catalog_with
from support.recorders import described

from xlf_translator.domain.auto_fill_report import AutoFillReport


def test_auto_filled_ordinals_are_named():
    report = AutoFillReport(catalog_with(60, default="untranslated", auto_filled=[30]))
    assert report.ordinals() == (30,)
    assert described(report)["auto_filled"] == (30,)
