class CatalogRefusal:
    """Why a document cannot be translated: what was expected and what was found."""

    def __init__(self, expected: str, found: str):
        self._expected = expected
        self._found = found

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CatalogRefusal) and str(self) == str(other)

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return f"Expected {self._expected}, found {self._found}."

    def __repr__(self) -> str:
        return f"CatalogRefusal({self._expected!r}, {self._found!r})"
