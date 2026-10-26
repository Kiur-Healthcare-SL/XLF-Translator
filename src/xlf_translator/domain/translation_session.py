from xlf_translator.domain.artifact_name import ArtifactName
from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.catalog_position import CatalogPosition
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.language_pair import LanguagePair
from xlf_translator.domain.unit_identifier import UnitIdentifier
from xlf_translator.domain.uploaded_document import UploadedDocument


class TranslationSession:
    """A translator's place in a catalog and the languages it is translated between.

    Movement of any kind is refused while the current unit is invalid.
    """

    def __init__(self, position: CatalogPosition, languages: LanguagePair):
        self._position = position
        self._languages = languages

    @staticmethod
    def resumed(catalog: Catalog, languages: LanguagePair) -> "TranslationSession":
        return TranslationSession(CatalogPosition.resumed(catalog), languages)

    def is_blocked(self) -> bool:
        return self._position.current().is_invalid()

    def forward(self) -> "TranslationSession":
        return self._moved_to(self._position.forward())

    def backward(self) -> "TranslationSession":
        return self._moved_to(self._position.backward())

    def jump(self, ordinal: int) -> "TranslationSession":
        return self._moved_to(self._position.jump(ordinal))

    def _moved_to(self, position: CatalogPosition) -> "TranslationSession":
        return self if self.is_blocked() else TranslationSession(position, self._languages)

    def contains(self, ordinal: int) -> bool:
        return self._position.contains(ordinal)

    def enter_target(self, identifier: UnitIdentifier, masked: str) -> "TranslationSession":
        return TranslationSession(self._position.with_target(identifier, masked), self._languages)

    def copy_source(self) -> "TranslationSession":
        return TranslationSession(self._position.with_source_copied(), self._languages)

    def needs_target_language(self) -> bool:
        return not self._languages.has_target()

    def choose_target_language(self, language: LanguageCode) -> "TranslationSession":
        return TranslationSession(self._position, self._languages.adopt_target(language))

    def is_complete(self) -> bool:
        return self._position.completion().is_complete()

    def draft_name(self, document: UploadedDocument) -> ArtifactName:
        return self._languages.draft_name(document)

    def final_name(self, document: UploadedDocument) -> ArtifactName:
        return self._languages.final_name(document)

    def write_with(self, writer, document: UploadedDocument) -> bytes:
        return self._languages.write_with(writer, document, self._position)

    def describe_into(self, builder) -> None:
        self._position.describe_into(builder)
        self._languages.describe_into(builder)
        builder.classification(self._position.classification().value)
        self._position.auto_fill().describe_into(builder)
        self._position.completion().describe_into(builder)

    def describe_current_into(self, builder) -> None:
        self._position.describe_into(builder)
        self._position.current().describe_into(builder)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TranslationSession) and (self._position, self._languages) == (
            other._position,
            other._languages,
        )

    def __hash__(self) -> int:
        return hash((self._position, self._languages))
