import streamlit as st

from xlf_translator.application.session_view import SessionView
from xlf_translator.domain.uploaded_document import UploadedDocument
from xlf_translator.presentation.screen_state import FINISH, TRANSLATE, ScreenState
from xlf_translator.presentation.use_cases import UseCases


def render_upload_screen(use_cases: UseCases, screen: ScreenState) -> None:
    st.title("XLF Translator")
    st.write("Upload an Angular XLIFF 1.2 catalog (`.xlf`, UTF-8, at most 4 MiB) to translate it one unit at a time.")
    upload = st.file_uploader("Catalog", type=["xlf"], key=screen.upload_key())
    if upload is None:
        return
    opened = use_cases.open_catalog.execute(UploadedDocument(upload.name, upload.getvalue()))
    if not isinstance(opened, SessionView):
        st.error(f"This file cannot be translated. {opened}")
        return
    screen.show(FINISH if opened.classification == "completed" else TRANSLATE)
    st.rerun()
