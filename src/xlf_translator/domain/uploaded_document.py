from xlf_translator.domain.artifact_name import ArtifactName
from xlf_translator.domain.document_size import DocumentSize
from xlf_translator.domain.language_code import LanguageCode

EXTENSION = ".xlf"
DRAFT_MARK = ".draft"


class UploadedDocument:
    """The bytes of an uploaded catalog and the stem of the name it came under."""

    def __init__(self, file_name: str, content: bytes):
        self._file_name = file_name
        self._content = content

    def size(self) -> DocumentSize:
        return DocumentSize(len(self._content))

    def draft_name(self, language: LanguageCode) -> ArtifactName:
        return ArtifactName.draft(self._stem(), language)

    def final_name(self, language: LanguageCode) -> ArtifactName:
        return ArtifactName.final(self._stem(), language)

    def _stem(self) -> str:
        return self._file_name.removesuffix(EXTENSION).removesuffix(DRAFT_MARK)

    def __bytes__(self) -> bytes:
        return self._content

    def __str__(self) -> str:
        return self._file_name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, UploadedDocument) and (self._file_name, self._content) == (other._file_name, other._content)

    def __hash__(self) -> int:
        return hash((self._file_name, self._content))
