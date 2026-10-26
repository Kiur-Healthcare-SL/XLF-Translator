from dataclasses import dataclass

from xlf_translator.application.unit_view import UnitView


@dataclass(frozen=True)
class Movement:
    """The unit current after a movement request, and why it was refused, if it was."""

    unit: UnitView
    refusal: tuple[str, ...] = ()

    def was_refused(self) -> bool:
        return self.refusal != ()
