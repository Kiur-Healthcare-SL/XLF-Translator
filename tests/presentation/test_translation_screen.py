from support.app_driver import button, go_to, position, texts, translating

from xlf_translator.application.unit_view import UnitView
from xlf_translator.presentation.translation_screen import target_key


def test_the_layout_shows_name_source_position_and_target():
    app = translating("messages.en-GB.xlf")
    assert texts(app.title) == ["messages.en-GB.xlf"]
    assert position(app) == "Item 31 of 60"
    assert "Exportar imágenes" in app.html[0].value
    assert app.text_area[0].key == "target::export.title"


def test_an_auto_filled_current_unit_is_marked():
    app = go_to(translating("messages.xlf"), 30)
    assert position(app) == "Item 30 of 60"
    assert any("auto-filled" in warning for warning in texts(app.warning))


def test_widgets_are_keyed_by_unit_so_text_does_not_leak():
    app = go_to(translating("messages.xlf"), 7)
    app.text_area[0].input("Reports").run()
    button(app, "Next").click().run()
    assert position(app) == "Item 8 of 60"
    assert app.text_area[0].key == "target::viewer.back"
    assert app.text_area[0].value == ""
    button(app, "Prev").click().run()
    assert app.text_area[0].value == "Reports"


def test_the_copy_button_puts_the_source_in_the_target():
    app = go_to(translating("messages.xlf"), 5)
    button(app, "Copy source").click().run()
    assert app.text_area[0].value == "Modo de {1}funcionalidad limitada{2} activo"


def test_the_gate_names_the_missing_token_and_disables_movement():
    app = go_to(translating("messages.en-GB.xlf"), 44)
    assert position(app) == "Item 44 of 60"
    assert "{1}" in app.error[0].value
    assert "<button mat-icon-button" in app.error[0].value
    assert all(button(app, label).disabled for label in ("Prev", "Next", "Go", "Finish"))


def test_clearing_an_invalid_target_releases_the_gate():
    app = go_to(translating("messages.en-GB.xlf"), 44)
    app.text_area[0].input("").run()
    assert not button(app, "Next").disabled
    button(app, "Next").click().run()
    assert position(app) == "Item 45 of 60"


def test_go_to_moves_within_range():
    assert position(go_to(translating("messages.en-GB.xlf"), 52)) == "Item 52 of 60"


def test_go_to_refuses_an_ordinal_outside_the_catalog():
    app = go_to(translating("messages.en-GB.xlf"), 500)
    assert position(app) == "Item 31 of 60"
    assert "There is no unit 500" in app.error[0].value


def test_save_draft_is_offered_while_units_are_invalid():
    app = go_to(translating("messages.en-GB.xlf"), 44)
    assert [download.label for download in app.download_button] == ["Save draft"]


def test_the_target_key_is_the_unit_identifier():
    unit = UnitView("viewer.back", 8, 60, "", "", "untranslated", False, ())
    assert target_key(unit) == "target::viewer.back"
