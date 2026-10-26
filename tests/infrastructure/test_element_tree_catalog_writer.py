from support.fixture_documents import FRESH, PARTIAL
from support.written_documents import NAMESPACE, children, parsed, trans_unit, written


def test_a_new_target_follows_its_source_without_state():
    unit = trans_unit(parsed(written(FRESH, app__title="CT Scan Analyser")), "app.title")
    assert children(unit) == ["source", "target", "context-group"]
    target = unit.find(f"{NAMESPACE}target")
    assert (target.text, target.get("state")) == ("CT Scan Analyser", None)


def test_a_new_target_carries_its_placeholders():
    unit = trans_unit(parsed(written(FRESH, viewer__limitedMode="{1}Limited{2} mode")), "viewer.limitedMode")
    target = unit.find(f"{NAMESPACE}target")
    assert [child.get("id") for child in target] == ["START_BOLD_TEXT", "CLOSE_BOLD_TEXT"]
    assert target[0].get("equiv-text") == "<b>"


def test_an_edited_imported_target_is_replaced():
    unit = trans_unit(parsed(written(PARTIAL, app__title="CT Analyser")), "app.title")
    targets = unit.findall(f"{NAMESPACE}target")
    assert [target.text for target in targets] == ["CT Analyser"]


def test_a_cleared_target_is_removed():
    unit = trans_unit(parsed(written(PARTIAL, app__title="")), "app.title")
    assert "target" not in children(unit)


def test_the_target_language_is_declared():
    file = parsed(written(FRESH)).find(f"{NAMESPACE}file")
    assert (file.get("source-language"), file.get("target-language")) == ("es", "en-GB")


def test_a_declared_target_language_is_replaced():
    file = parsed(written(PARTIAL, language="en-US")).find(f"{NAMESPACE}file")
    assert file.get("target-language") == "en-US"


def test_an_auto_filled_unit_is_written_as_edited():
    unit = trans_unit(parsed(written(FRESH)), "layout.spacer")
    assert unit.find(f"{NAMESPACE}target").text == "   "


def test_the_output_is_utf_8_with_angular_style_empty_elements():
    output = written(FRESH, viewer__limitedMode="{1}Limited{2} mode")
    assert output.startswith(b'<?xml version="1.0" encoding="UTF-8"?>')
    assert b" />" not in output
    assert "Analizador".encode("utf-8") in output
