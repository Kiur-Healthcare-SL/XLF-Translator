from xlf_translator.domain.catalog_refusal import CatalogRefusal

LIMIT_IN_BYTES = 4 * 1024 * 1024


class DocumentSize:
    """The size of an uploaded document, checked against the 4 MiB limit."""

    def __init__(self, byte_count: int):
        self._byte_count = byte_count

    def is_within_limit(self) -> bool:
        return self._byte_count <= LIMIT_IN_BYTES

    def refusal(self) -> CatalogRefusal:
        return CatalogRefusal(
            f"a document of at most 4 MiB ({LIMIT_IN_BYTES:,} bytes)",
            f"{self._byte_count:,} bytes",
        )

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DocumentSize) and self._byte_count == other._byte_count

    def __hash__(self) -> int:
        return hash(self._byte_count)
