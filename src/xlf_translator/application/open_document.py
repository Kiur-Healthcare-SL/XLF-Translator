from collections.abc import Callable

from xlf_translator.application.export_artifact import ExportArtifact
from xlf_translator.application.export_refusal import ExportRefusal
from xlf_translator.application.session_view import SessionView
from xlf_translator.application.session_view_builder import SessionViewBuilder
from xlf_translator.application.unit_view import UnitView
from xlf_translator.application.unit_view_builder import UnitViewBuilder
from xlf_translator.domain.translation_session import TranslationSession
from xlf_translator.domain.uploaded_document import UploadedDocument

SessionChange = Callable[[TranslationSession], TranslationSession]
SessionQuestion = Callable[[TranslationSession], bool]


class OpenDocument:
    """The uploaded document and the translation session opened from it."""

    def __init__(self, document: UploadedDocument, session: TranslationSession):
        self._document = document
        self._session = session

    def changed(self, change: SessionChange) -> "OpenDocument":
        return OpenDocument(self._document, change(self._session))

    def answers(self, question: SessionQuestion) -> bool:
        return question(self._session)

    def describe(self) -> SessionView:
        builder = SessionViewBuilder(str(self._document))
        self._session.describe_into(builder)
        return builder.build()

    def describe_current(self) -> UnitView:
        builder = UnitViewBuilder()
        self._session.describe_current_into(builder)
        return builder.build()

    def export_draft(self, writer) -> ExportArtifact:
        name = self._session.draft_name(self._document)
        return ExportArtifact(str(name), self._session.write_with(writer, self._document))

    def export_final(self, writer) -> ExportArtifact | ExportRefusal:
        view = self.describe()
        if not view.is_complete():
            return ExportRefusal(view.untranslated, view.invalid)
        name = self._session.final_name(self._document)
        return ExportArtifact(str(name), self._session.write_with(writer, self._document))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, OpenDocument) and (self._document, self._session) == (other._document, other._session)

    def __hash__(self) -> int:
        return hash((self._document, self._session))
