from abc import ABC, abstractmethod

from xlf_translator.application.open_document import OpenDocument


class SessionRepository(ABC):
    """Port: holds the document being translated between reruns of the page."""

    @abstractmethod
    def load(self) -> OpenDocument | None:
        """Answer the open document, or None when no session is open."""

    @abstractmethod
    def save(self, open_document: OpenDocument) -> None:
        """Keep the open document for the next rerun."""

    @abstractmethod
    def clear(self) -> None:
        """Forget the open document."""
