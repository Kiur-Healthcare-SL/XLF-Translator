import streamlit as st

from xlf_translator.application.session_view import SessionView
from xlf_translator.presentation.screen_state import ScreenState
from xlf_translator.presentation.use_cases import UseCases


def render_auto_fill_notice(session: SessionView) -> None:
    if not session.auto_filled:
        return
    ordinals = ", ".join(str(ordinal) for ordinal in session.auto_filled)
    st.info(f"Auto-filled because their source is only whitespace: unit {ordinals}. Check them before finishing.")


def render_message(screen: ScreenState) -> None:
    for line in screen.take_message():
        st.error(line)


def render_draft_download(use_cases: UseCases) -> None:
    draft = use_cases.export_draft.execute()
    st.download_button("Save draft", draft.content, file_name=draft.name, mime="application/xml", key="save-draft")
