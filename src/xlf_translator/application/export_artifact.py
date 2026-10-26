from dataclasses import dataclass


@dataclass(frozen=True)
class ExportArtifact:
    """A document ready for the browser's save dialog."""

    name: str
    content: bytes
