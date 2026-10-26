"""Composition root: `streamlit run src/xlf_translator/presentation/app.py`."""

import streamlit as st

from xlf_translator.infrastructure.element_tree_catalog_reader import ElementTreeCatalogReader
from xlf_translator.infrastructure.element_tree_catalog_writer import ElementTreeCatalogWriter
from xlf_translator.presentation.completed_screen import render_completed_screen
from xlf_translator.presentation.guide_screen import render_guide_screen
from xlf_translator.presentation.language_form import render_language_form
from xlf_translator.presentation.screen_state import FINISH, GUIDE, ScreenState
from xlf_translator.presentation.session_state_session_repository import SessionStateSessionRepository
from xlf_translator.presentation.translation_screen import render_translation_screen
from xlf_translator.presentation.upload_screen import render_upload_screen
from xlf_translator.presentation.use_cases import UseCases


def main() -> None:
    st.set_page_config(page_title="XLF Translator", layout="wide")
    repository = SessionStateSessionRepository(st.session_state)
    use_cases = UseCases.wired(repository, ElementTreeCatalogReader(), ElementTreeCatalogWriter())
    screen = ScreenState(st.session_state)
    if screen.current() != GUIDE:
        st.sidebar.button("How it works", on_click=screen.open_guide)
    route(use_cases, screen)


def route(use_cases: UseCases, screen: ScreenState) -> None:
    if screen.current() == GUIDE:
        render_guide_screen(screen)
        return
    if not use_cases.show.is_open():
        render_upload_screen(use_cases, screen)
        return
    session = use_cases.show.session()
    if session.needs_target_language():
        render_language_form(use_cases, session)
        return
    if screen.current() == FINISH:
        render_completed_screen(use_cases, screen)
        return
    render_translation_screen(use_cases, screen)


if __name__ == "__main__":
    main()
