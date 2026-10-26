from support.catalog_samples import catalog_with
from support.fakes import RecordingCatalogWriter
from support.session_samples import repository_over

from xlf_translator.application.export_draft import ExportDraft


def test_a_draft_is_exported_while_units_are_untranslated_or_invalid():
    repository = repository_over(catalog_with(60, untranslated=[31], invalid=[44]))
    artifact = ExportDraft(repository, RecordingCatalogWriter()).execute()
    assert artifact.name == "messages.en-GB.draft.xlf"
    assert artifact.content == b"messages.xlf:en-GB"
