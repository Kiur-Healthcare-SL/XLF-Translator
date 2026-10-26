from xlf_translator.domain.language_code import LanguageCode

EXTENSION = ".xlf"
DRAFT_MARK = ".draft"


class ArtifactName:
    """The file name an export is offered under: `<stem>.<language>[.draft].xlf`."""

    def __init__(self, value: str):
        self._value = value

    @staticmethod
    def draft(stem: str, language: LanguageCode) -> "ArtifactName":
        return ArtifactName(f"{ArtifactName._bare(stem, language)}.{language}{DRAFT_MARK}{EXTENSION}")

    @staticmethod
    def final(stem: str, language: LanguageCode) -> "ArtifactName":
        return ArtifactName(f"{ArtifactName._bare(stem, language)}.{language}{EXTENSION}")

    @staticmethod
    def _bare(stem: str, language: LanguageCode) -> str:
        """A re-uploaded `messages.fr` stem already names its language once."""
        return stem.removesuffix(f".{language}")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ArtifactName) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"ArtifactName({self._value!r})"
