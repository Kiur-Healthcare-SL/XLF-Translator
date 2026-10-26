from xlf_translator.application.session_view import SessionView


class SessionViewBuilder:
    """Collects what a session tells about itself into a `SessionView`."""

    def __init__(self, document_name: str):
        self._fields = {"document_name": document_name}

    def position(self, ordinal: int, total: int) -> None:
        self._fields.update(ordinal=ordinal, total=total)

    def languages(self, source: str, target: str | None) -> None:
        self._fields.update(source_language=source, target_language=target)

    def classification(self, classification: str) -> None:
        self._fields.update(classification=classification)

    def auto_filled(self, ordinals: tuple[int, ...]) -> None:
        self._fields.update(auto_filled=ordinals)

    def completion(self, untranslated: tuple[int, ...], invalid: tuple[int, ...]) -> None:
        self._fields.update(untranslated=untranslated, invalid=invalid)

    def build(self) -> SessionView:
        return SessionView(**self._fields)
