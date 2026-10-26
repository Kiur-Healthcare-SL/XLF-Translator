from support.fixture_documents import COMPLETED
from support.real_wiring import opened


def test_the_completed_fixture_adopts_french_and_exports_its_final_name():
    use_cases, view = opened(COMPLETED)
    assert view.classification == "completed"
    assert view.target_language == "fr"
    assert not view.needs_target_language()
    artifact = use_cases.export_final.execute()
    assert artifact.name == "messages.fr.xlf"
    assert b'target-language="fr"' in artifact.content
