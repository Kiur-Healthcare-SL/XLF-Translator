from xlf_translator.application.session_repository import SessionRepository
from xlf_translator.application.session_view import SessionView
from xlf_translator.application.unit_view import UnitView


class ShowSession:
    """Describes the open session and its current unit, for a screen to render."""

    def __init__(self, repository: SessionRepository):
        self._repository = repository

    def is_open(self) -> bool:
        return self._repository.load() is not None

    def session(self) -> SessionView:
        return self._repository.load().describe()

    def current_unit(self) -> UnitView:
        return self._repository.load().describe_current()
