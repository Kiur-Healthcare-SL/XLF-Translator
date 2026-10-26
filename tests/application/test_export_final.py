from support.catalog_samples import catalog_with
from support.fakes import RecordingCatalogWriter
from support.session_samples import repository_over

from xlf_translator.application.export_artifact import ExportArtifact
from xlf_translator.application.export_final import ExportFinal


def exported(catalog):
    writer = RecordingCatalogWriter()
    return ExportFinal(repository_over(catalog), writer).execute(), writer


def test_a_final_export_is_refused_naming_untranslated_and_invalid_ordinals():
    refusal, writer = exported(catalog_with(60, untranslated=[31, 38], invalid=[44, 52]))
    assert refusal.unresolved() == (31, 38, 44, 52)
    assert writer.calls == []


def test_a_complete_catalog_is_exported_under_its_final_name():
    artifact, _ = exported(catalog_with(60, auto_filled=[30]))
    assert artifact == ExportArtifact("messages.en-GB.xlf", b"messages.xlf:en-GB")
