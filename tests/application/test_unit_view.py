from xlf_translator.application.unit_view import UnitView


def view(state):
    return UnitView("unit.1", 1, 60, "{1}a{2}", "{1}", state, False, ("{2} (</b>) is missing",))


def test_a_view_knows_when_its_unit_is_invalid():
    assert view("invalid").is_invalid()
    assert not view("translated").is_invalid()
