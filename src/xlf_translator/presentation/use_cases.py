from dataclasses import dataclass

from xlf_translator.application.catalog_reader import CatalogReader
from xlf_translator.application.catalog_writer import CatalogWriter
from xlf_translator.application.choose_target_language import ChooseTargetLanguage
from xlf_translator.application.copy_source_into_target import CopySourceIntoTarget
from xlf_translator.application.enter_target import EnterTarget
from xlf_translator.application.export_draft import ExportDraft
from xlf_translator.application.export_final import ExportFinal
from xlf_translator.application.move_to_unit import MoveToUnit
from xlf_translator.application.open_catalog import OpenCatalog
from xlf_translator.application.session_repository import SessionRepository
from xlf_translator.application.show_session import ShowSession


@dataclass(frozen=True)
class UseCases:
    """Every use case a screen may call, wired to one repository, reader and writer."""

    repository: SessionRepository
    open_catalog: OpenCatalog
    choose_target_language: ChooseTargetLanguage
    move: MoveToUnit
    enter_target: EnterTarget
    copy_source: CopySourceIntoTarget
    export_draft: ExportDraft
    export_final: ExportFinal
    show: ShowSession

    @staticmethod
    def wired(repository: SessionRepository, reader: CatalogReader, writer: CatalogWriter) -> "UseCases":
        return UseCases(
            repository,
            OpenCatalog(reader, repository),
            ChooseTargetLanguage(repository),
            MoveToUnit(repository),
            EnterTarget(repository),
            CopySourceIntoTarget(repository),
            ExportDraft(repository, writer),
            ExportFinal(repository, writer),
            ShowSession(repository),
        )
