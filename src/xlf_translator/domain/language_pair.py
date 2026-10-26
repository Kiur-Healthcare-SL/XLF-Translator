from xlf_translator.domain.artifact_name import ArtifactName
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.uploaded_document import UploadedDocument


class LanguagePair:
    """The source language of a catalog and, once known, its target language."""

    def __init__(self, source: LanguageCode, target: LanguageCode | None = None):
        self._source = source
        self._target = target

    def has_target(self) -> bool:
        return self._target is not None

    def adopt_target(self, target: LanguageCode) -> "LanguagePair":
        return LanguagePair(self._source, target)

    def describe_into(self, builder) -> None:
        builder.languages(str(self._source), self._target and str(self._target))

    def draft_name(self, document: UploadedDocument) -> ArtifactName:
        return document.draft_name(self._target)

    def final_name(self, document: UploadedDocument) -> ArtifactName:
        return document.final_name(self._target)

    def write_with(self, writer, document: UploadedDocument, position) -> bytes:
        return position.write_with(writer, document, self._target)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, LanguagePair) and (self._source, self._target) == (other._source, other._target)

    def __hash__(self) -> int:
        return hash((self._source, self._target))

    def __repr__(self) -> str:
        return f"LanguagePair({self._source!r}, {self._target!r})"
