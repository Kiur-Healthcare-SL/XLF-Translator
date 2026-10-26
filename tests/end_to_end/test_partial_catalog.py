from support.fixture_documents import PARTIAL
from support.real_wiring import opened

from xlf_translator.application.export_refusal import ExportRefusal


def test_the_partial_fixture_resumes_at_its_first_gap_and_refuses_a_final_export():
    use_cases, view = opened(PARTIAL)
    assert view.classification == "partial"
    assert view.target_language == "en-GB"
    assert view.ordinal == 31
    refusal = use_cases.export_final.execute()
    assert isinstance(refusal, ExportRefusal)
    assert refusal.unresolved() == (31, 38, 44, 52)


def test_repairing_the_partial_fixture_permits_the_final_export():
    use_cases, _ = opened(PARTIAL)
    use_cases.enter_target.execute("export.title", "Export images")
    use_cases.enter_target.execute("report.title", "Radiology report")
    use_cases.copy_source.execute()
    use_cases.move.jump(44)
    use_cases.enter_target.execute("viewer.close", "{1}{2}close{3} Close viewer{4}")
    use_cases.enter_target.execute(
        "8c2e5a7f1d3b9e0a4c6f8b2d0e1a3c5f7b9d2e4a", "{1} of {2} slices processed"
    )
    artifact = use_cases.export_final.execute()
    assert artifact.name == "messages.en-GB.xlf"
