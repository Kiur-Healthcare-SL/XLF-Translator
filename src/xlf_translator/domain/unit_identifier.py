class UnitIdentifier:
    """The id a trans-unit declares; unique within a catalog."""

    def __init__(self, value: str):
        if not value.strip():
            raise ValueError("A unit identifier cannot be empty")
        self._value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UnitIdentifier) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f"UnitIdentifier({self._value!r})"
