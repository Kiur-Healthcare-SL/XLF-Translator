from xlf_translator.application.movement import Movement
from xlf_translator.application.open_document import SessionChange
from xlf_translator.application.session_repository import SessionRepository


class MoveToUnit:
    """Moves to the previous, next or a chosen unit, unless the current one is invalid."""

    def __init__(self, repository: SessionRepository):
        self._repository = repository

    def forward(self) -> Movement:
        return self._move(lambda session: session.forward())

    def backward(self) -> Movement:
        return self._move(lambda session: session.backward())

    def jump(self, ordinal: int) -> Movement:
        open_document = self._repository.load()
        if not open_document.answers(lambda session: session.contains(ordinal)):
            total = open_document.describe().total
            return Movement(open_document.describe_current(), (f"There is no unit {ordinal}; choose 1 to {total}.",))
        return self._move(lambda session: session.jump(ordinal))

    def _move(self, change: SessionChange) -> Movement:
        open_document = self._repository.load()
        if open_document.answers(lambda session: session.is_blocked()):
            current = open_document.describe_current()
            return Movement(current, current.problems)
        moved = open_document.changed(change)
        self._repository.save(moved)
        return Movement(moved.describe_current())
