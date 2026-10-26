import re

BCP_47_SHAPE = re.compile(r"[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*")


class LanguageCode:
    """A BCP 47-shaped language tag such as `es`, `fr` or `en-GB`."""

    def __init__(self, value: str):
        if not LanguageCode.accepts(value):
            raise ValueError(f"Not a language code: {value!r}")
        self._value = value

    @staticmethod
    def accepts(value: str) -> bool:
        return BCP_47_SHAPE.fullmatch(value) is not None

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LanguageCode) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"LanguageCode({self._value!r})"
