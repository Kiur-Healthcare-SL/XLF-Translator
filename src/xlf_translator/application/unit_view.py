from dataclasses import dataclass


@dataclass(frozen=True)
class UnitView:
    """What the screen shows of one unit; built by `UnitViewBuilder` (design D4)."""

    identifier: str
    ordinal: int
    total: int
    source: str
    target: str
    state: str
    auto_filled: bool
    problems: tuple[str, ...]

    def is_invalid(self) -> bool:
        return self.state == "invalid"
