import streamlit as st

from xlf_translator.application.export_artifact import ExportArtifact
from xlf_translator.application.session_view import SessionView
from xlf_translator.presentation.screen_state import TRANSLATE, ScreenState
from xlf_translator.presentation.session_notices import render_auto_fill_notice, render_draft_download, render_message
from xlf_translator.presentation.translation_screen import move
from xlf_translator.presentation.use_cases import UseCases


def render_completed_screen(use_cases: UseCases, screen: ScreenState) -> None:
    session = use_cases.show.session()
    st.title(session.document_name)
    render_auto_fill_notice(session)
    render_message(screen)
    render_export(use_cases, screen, session)
    st.button("Back to translation", on_click=screen.show, args=(TRANSLATE,))
    render_draft_download(use_cases)


def render_export(use_cases: UseCases, screen: ScreenState, session: SessionView) -> None:
    final = use_cases.export_final.execute()
    if isinstance(final, ExportArtifact):
        render_final_download(use_cases, screen, final)
        return
    render_unresolved(use_cases, screen, session)


def render_final_download(use_cases: UseCases, screen: ScreenState, final: ExportArtifact) -> None:
    st.success(f"Every unit is translated. Download {final.name} to finish.")
    st.download_button(
        "Download", final.content, file_name=final.name, mime="application/xml", on_click=screen.request_final_export
    )
    if screen.final_export_requested():
        st.button("Upload another file", on_click=start_over, args=(use_cases, screen))


def render_unresolved(use_cases: UseCases, screen: ScreenState, session: SessionView) -> None:
    st.error("Download is refused until every unit is translated and its tokens match its source.")
    for ordinal in session.unresolved():
        reason = "untranslated" if ordinal in session.untranslated else "tokens do not match"
        st.button(f"Go to item {ordinal} ({reason})", key=f"unresolved-{ordinal}", on_click=jump, args=(use_cases, screen, ordinal))


def jump(use_cases: UseCases, screen: ScreenState, ordinal: int) -> None:
    move(screen, lambda: use_cases.move.jump(ordinal))
    screen.show(TRANSLATE)


def start_over(use_cases: UseCases, screen: ScreenState) -> None:
    use_cases.repository.clear()
    screen.start_over()
