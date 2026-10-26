from xlf_translator.domain.catalog import Catalog


class CompletionReport:
    """Whether every unit is translated, and if not, which ordinals are not."""

    def __init__(self, catalog: Catalog):
        self._catalog = catalog

    def is_complete(self) -> bool:
        return self._catalog.every(lambda unit: unit.is_translated())

    def untranslated(self) -> tuple[int, ...]:
        return self._catalog.ordinals_where(lambda unit: unit.is_untranslated())

    def invalid(self) -> tuple[int, ...]:
        return self._catalog.ordinals_where(lambda unit: unit.is_invalid())

    def unresolved(self) -> tuple[int, ...]:
        return self._catalog.ordinals_where(lambda unit: unit.is_unresolved())

    def describe_into(self, builder) -> None:
        builder.completion(self.untranslated(), self.invalid())
