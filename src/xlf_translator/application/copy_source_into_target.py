from xlf_translator.application.session_repository import SessionRepository
from xlf_translator.application.unit_view import UnitView


class CopySourceIntoTarget:
    """Replaces the current unit's target with its source, every character included."""

    def __init__(self, repository: SessionRepository):
        self._repository = repository

    def execute(self) -> UnitView:
        open_document = self._repository.load().changed(lambda session: session.copy_source())
        self._repository.save(open_document)
        return open_document.describe_current()
