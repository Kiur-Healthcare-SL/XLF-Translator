from dataclasses import dataclass


@dataclass(frozen=True)
class ExportRefusal:
    """Why a final export was refused: the ordinals still needing work."""

    untranslated: tuple[int, ...]
    invalid: tuple[int, ...]

    def unresolved(self) -> tuple[int, ...]:
        return tuple(sorted(self.untranslated + self.invalid))
