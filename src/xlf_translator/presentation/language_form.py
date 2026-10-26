import streamlit as st

from xlf_translator.application.session_view import SessionView
from xlf_translator.presentation.use_cases import UseCases


def render_language_form(use_cases: UseCases, session: SessionView) -> None:
    st.title(session.document_name)
    st.write(f"This catalog is in `{session.source_language}` and declares no target language.")
    with st.form("target-language"):
        language = st.text_input("Target language", placeholder="en-GB")
        submitted = st.form_submit_button("Start translating")
    if not submitted:
        return
    chosen = use_cases.choose_target_language.execute(language.strip())
    if not isinstance(chosen, SessionView):
        st.error(str(chosen))
        return
    st.rerun()
