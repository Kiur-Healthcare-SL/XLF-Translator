from collections.abc import Callable

import streamlit as st

from xlf_translator.application.movement import Movement
from xlf_translator.application.unit_view import UnitView
from xlf_translator.presentation.screen_state import FINISH, TRANSLATE, ScreenState
from xlf_translator.presentation.session_notices import render_auto_fill_notice, render_draft_download, render_message
from xlf_translator.presentation.use_cases import UseCases
from xlf_translator.presentation.whitespace_marker import WhitespaceMarker


def target_key(unit: UnitView) -> str:
    return f"target::{unit.identifier}"


def render_translation_screen(use_cases: UseCases, screen: ScreenState) -> None:
    session = use_cases.show.session()
    unit = use_cases.show.current_unit()
    st.title(session.document_name)
    render_auto_fill_notice(session)
    render_message(screen)
    source_column, target_column = st.columns(2)
    with source_column:
        render_source(unit)
    with target_column:
        render_target(use_cases, unit)
    render_gate(unit)
    render_navigation(use_cases, screen, unit)


def render_source(unit: UnitView) -> None:
    st.caption("Source")
    st.html(WhitespaceMarker().block(unit.source))


def render_target(use_cases: UseCases, unit: UnitView) -> None:
    st.caption(f"Item {unit.ordinal} of {unit.total}")
    key = target_key(unit)
    if key not in st.session_state:
        st.session_state[key] = unit.target
    st.text_area("Target", key=key, on_change=enter_target, args=(use_cases, unit.identifier, key))
    if unit.auto_filled:
        st.warning("This unit was auto-filled: its source is only whitespace, so its target is the source.")


def render_gate(unit: UnitView) -> None:
    if not unit.is_invalid():
        return
    problems = "; ".join(unit.problems)
    st.error(f"You cannot leave this unit until its tokens match the source: {problems}. Fix them or clear the target.")


def render_navigation(use_cases: UseCases, screen: ScreenState, unit: UnitView) -> None:
    blocked = unit.is_invalid()
    previous, following, copy, finish = st.columns(4)
    previous.button("Prev", disabled=blocked, on_click=move, args=(screen, use_cases.move.backward))
    following.button("Next", disabled=blocked, on_click=move, args=(screen, use_cases.move.forward))
    copy.button("Copy source", on_click=copy_source, args=(use_cases, unit))
    finish.button("Finish", disabled=blocked, on_click=screen.show, args=(FINISH,))
    render_go_to(use_cases, screen, unit, blocked)
    render_draft_download(use_cases)


def render_go_to(use_cases: UseCases, screen: ScreenState, unit: UnitView, blocked: bool) -> None:
    ordinal_column, button_column = st.columns([3, 1])
    ordinal_column.number_input("Go to item", min_value=1, step=1, value=unit.ordinal, key="go-to-ordinal")
    button_column.button("Go", disabled=blocked, on_click=go_to, args=(use_cases, screen))


def enter_target(use_cases: UseCases, identifier: str, key: str) -> None:
    use_cases.enter_target.execute(identifier, st.session_state[key])


def copy_source(use_cases: UseCases, unit: UnitView) -> None:
    copied = use_cases.copy_source.execute()
    st.session_state[target_key(unit)] = copied.target


def move(screen: ScreenState, movement: Callable[[], Movement]) -> None:
    moved = movement()
    screen.tell(moved.refusal)
    st.session_state.pop("go-to-ordinal", None)


def go_to(use_cases: UseCases, screen: ScreenState) -> None:
    move(screen, lambda: use_cases.move.jump(int(st.session_state["go-to-ordinal"])))
    screen.show(TRANSLATE)
