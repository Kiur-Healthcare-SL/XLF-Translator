from support.catalog_samples import catalog_with
from support.fakes import RecordingCatalogWriter
from support.session_samples import open_document

from xlf_translator.application.export_artifact import ExportArtifact
from xlf_translator.application.export_refusal import ExportRefusal


def test_a_change_yields_a_new_open_document():
    original = open_document(catalog_with(3))
    moved = original.changed(lambda session: session.forward())
    assert moved.describe().ordinal == 2
    assert original.describe().ordinal == 1


def test_an_open_document_answers_questions_about_its_session():
    assert open_document(catalog_with(3, invalid=[1])).answers(lambda session: session.is_blocked())


def test_a_draft_is_exported_whatever_the_state():
    artifact = open_document(catalog_with(3, invalid=[1])).export_draft(RecordingCatalogWriter())
    assert artifact == ExportArtifact("messages.en-GB.draft.xlf", b"messages.xlf:en-GB")


def test_a_final_export_is_refused_while_incomplete():
    refusal = open_document(catalog_with(3, untranslated=[2], invalid=[3])).export_final(RecordingCatalogWriter())
    assert refusal == ExportRefusal((2,), (3,))
