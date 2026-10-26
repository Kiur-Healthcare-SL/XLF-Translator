from xlf_translator.application.movement import Movement
from xlf_translator.application.unit_view import UnitView

UNIT = UnitView("unit.1", 1, 1, "a", "b", "translated", False, ())


def test_a_movement_without_refusal_was_permitted():
    assert not Movement(UNIT).was_refused()
    assert Movement(UNIT, ("{2} (</b>) is missing",)).was_refused()
