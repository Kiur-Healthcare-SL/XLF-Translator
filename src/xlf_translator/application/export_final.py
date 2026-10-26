from xlf_translator.application.catalog_writer import CatalogWriter
from xlf_translator.application.export_artifact import ExportArtifact
from xlf_translator.application.export_refusal import ExportRefusal
from xlf_translator.application.session_repository import SessionRepository


class ExportFinal:
    """Exports the finished catalog, refused while any unit is untranslated or invalid."""

    def __init__(self, repository: SessionRepository, writer: CatalogWriter):
        self._repository = repository
        self._writer = writer

    def execute(self) -> ExportArtifact | ExportRefusal:
        return self._repository.load().export_final(self._writer)
