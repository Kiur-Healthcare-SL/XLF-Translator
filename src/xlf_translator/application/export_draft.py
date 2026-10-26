from xlf_translator.application.catalog_writer import CatalogWriter
from xlf_translator.application.export_artifact import ExportArtifact
from xlf_translator.application.session_repository import SessionRepository


class ExportDraft:
    """Exports work in progress, whatever state its units are in."""

    def __init__(self, repository: SessionRepository, writer: CatalogWriter):
        self._repository = repository
        self._writer = writer

    def execute(self) -> ExportArtifact:
        return self._repository.load().export_draft(self._writer)
