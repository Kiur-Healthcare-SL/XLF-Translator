from support.catalog_samples import catalog_with
from support.session_samples import repository_over

from xlf_translator.application.move_to_unit import MoveToUnit


def test_stepwise_movement():
    moves = MoveToUnit(repository_over(catalog_with(60)))
    assert moves.forward().unit.ordinal == 2
    assert moves.forward().unit.ordinal == 3
    assert moves.backward().unit.ordinal == 2


def test_already_translated_units_offer_their_target():
    movement = MoveToUnit(repository_over(catalog_with(60))).forward()
    assert movement.unit.target == "{1}done{2}"


def test_jumping_to_an_ordinal():
    movement = MoveToUnit(repository_over(catalog_with(60))).jump(52)
    assert movement.unit.ordinal == 52
    assert not movement.was_refused()


def test_jumping_outside_the_catalog_is_refused():
    movement = MoveToUnit(repository_over(catalog_with(60))).jump(500)
    assert movement.unit.ordinal == 1
    assert movement.refusal == ("There is no unit 500; choose 1 to 60.",)


def test_movement_is_refused_while_the_current_unit_is_invalid():
    repository = repository_over(catalog_with(60, invalid=[44]))
    moves = MoveToUnit(repository)
    for movement in (moves.forward(), moves.backward(), moves.jump(7)):
        assert movement.unit.ordinal == 44
        assert movement.refusal == ("{2} (</b>) is missing",)
