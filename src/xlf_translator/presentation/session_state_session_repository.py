from collections.abc import MutableMapping

from xlf_translator.application.open_document import OpenDocument
from xlf_translator.application.session_repository import SessionRepository

OPEN_DOCUMENT_KEY = "xlf_translator.open_document"


class SessionStateSessionRepository(SessionRepository):
    """Keeps the open document in Streamlit's session state, apart from any widget key."""

    def __init__(self, state: MutableMapping):
        self._state = state

    def load(self) -> OpenDocument | None:
        return self._state.get(OPEN_DOCUMENT_KEY)

    def save(self, open_document: OpenDocument) -> None:
        self._state[OPEN_DOCUMENT_KEY] = open_document

    def clear(self) -> None:
        self._state.pop(OPEN_DOCUMENT_KEY, None)
