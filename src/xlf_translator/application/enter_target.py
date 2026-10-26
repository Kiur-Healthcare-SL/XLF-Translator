from xlf_translator.application.session_repository import SessionRepository
from xlf_translator.application.unit_view import UnitView
from xlf_translator.domain.unit_identifier import UnitIdentifier


class EnterTarget:
    """Records the target typed for a unit, named by its identifier (design D8)."""

    def __init__(self, repository: SessionRepository):
        self._repository = repository

    def execute(self, identifier: str, masked_target: str) -> UnitView:
        unit = UnitIdentifier(identifier)
        open_document = self._repository.load().changed(lambda session: session.enter_target(unit, masked_target))
        self._repository.save(open_document)
        return open_document.describe_current()
