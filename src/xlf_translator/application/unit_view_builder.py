from xlf_translator.application.unit_view import UnitView


class UnitViewBuilder:
    """Collects what a session tells about its current unit into a `UnitView`."""

    def __init__(self):
        self._fields = {}

    def identifier(self, identifier: str) -> None:
        self._fields.update(identifier=identifier)

    def position(self, ordinal: int, total: int) -> None:
        self._fields.update(ordinal=ordinal, total=total)

    def texts(self, source: str, target: str) -> None:
        self._fields.update(source=source, target=target)

    def state(self, state: str, auto_filled: bool, problems: tuple[str, ...]) -> None:
        self._fields.update(state=state, auto_filled=auto_filled, problems=problems)

    def build(self) -> UnitView:
        return UnitView(**self._fields)
