from xlf_translator.application.export_refusal import ExportRefusal


def test_a_refusal_names_every_unresolved_ordinal_in_order():
    assert ExportRefusal((31, 38), (44, 52)).unresolved() == (31, 38, 44, 52)
