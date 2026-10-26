from xlf_translator.domain.catalog import Catalog


class AutoFillReport:
    """The ordinals of units auto-filled because their source is only whitespace."""

    def __init__(self, catalog: Catalog):
        self._catalog = catalog

    def ordinals(self) -> tuple[int, ...]:
        return self._catalog.ordinals_where(lambda unit: unit.is_auto_filled())

    def describe_into(self, builder) -> None:
        builder.auto_filled(self.ordinals())
