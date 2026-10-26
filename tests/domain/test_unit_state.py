from xlf_translator.domain.unit_state import UnitState


def test_states_render_as_words():
    assert [state.value for state in UnitState] == ["translated", "untranslated", "invalid"]
