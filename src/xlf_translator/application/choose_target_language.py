from xlf_translator.application.session_repository import SessionRepository
from xlf_translator.application.session_view import SessionView
from xlf_translator.domain.catalog_refusal import CatalogRefusal
from xlf_translator.domain.language_code import LanguageCode


class ChooseTargetLanguage:
    """Sets the target language a fresh catalog is translated into (see note N3)."""

    def __init__(self, repository: SessionRepository):
        self._repository = repository

    def execute(self, language: str) -> SessionView | CatalogRefusal:
        if not LanguageCode.accepts(language):
            return CatalogRefusal("a language code such as en-GB", f"'{language}'")
        chosen = LanguageCode(language)
        open_document = self._repository.load().changed(lambda session: session.choose_target_language(chosen))
        self._repository.save(open_document)
        return open_document.describe()
