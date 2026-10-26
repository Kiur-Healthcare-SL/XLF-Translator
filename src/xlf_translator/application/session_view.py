from dataclasses import dataclass


@dataclass(frozen=True)
class SessionView:
    """What the screen shows of a session; built by `SessionViewBuilder` (design D4)."""

    document_name: str
    ordinal: int
    total: int
    source_language: str
    target_language: str | None
    classification: str
    auto_filled: tuple[int, ...]
    untranslated: tuple[int, ...]
    invalid: tuple[int, ...]

    def needs_target_language(self) -> bool:
        return self.target_language is None

    def is_complete(self) -> bool:
        return not self.unresolved()

    def unresolved(self) -> tuple[int, ...]:
        return tuple(sorted(self.untranslated + self.invalid))
