from support.catalog_samples import catalog_with
from support.session_samples import open_document

from xlf_translator.application.unit_view import UnitView
from xlf_translator.application.unit_view_builder import UnitViewBuilder


def test_a_unit_describes_itself_into_a_view():
    builder = UnitViewBuilder()
    builder.identifier("unit.30")
    builder.position(30, 60)
    builder.texts("   ", "   ")
    builder.state("translated", True, ())
    assert builder.build() == UnitView("unit.30", 30, 60, "   ", "   ", "translated", True, ())


def test_an_auto_filled_current_unit_carries_its_mark():
    unit = open_document(catalog_with(60, auto_filled=[30])).changed(lambda session: session.jump(30))
    view = unit.describe_current()
    assert (view.ordinal, view.auto_filled, view.state) == (30, True, "translated")
