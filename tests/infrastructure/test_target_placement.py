from support.fixture_documents import PARTIAL, fixture, read
from support.written_documents import children

from xlf_translator.domain.unit_identifier import UnitIdentifier
from xlf_translator.infrastructure.target_placement import TargetPlacement
from xlf_translator.infrastructure.xliff_document import XliffDocument


def placed(identifier, masked):
    xliff = XliffDocument.parse(bytes(fixture(PARTIAL)))
    elements = {element.get("id"): element for element in xliff.root().iter(xliff.tag("trans-unit"))}
    catalog, _ = read(PARTIAL)
    catalog.with_target(UnitIdentifier(identifier), masked).write_into(TargetPlacement(xliff, elements))
    return elements[identifier]


def test_an_unedited_target_is_left_alone():
    element = placed("app.subtitle", "Viewing and analysis of computed tomography scans")
    assert element.find(".//{*}target").get("state") == "translated"


def test_an_edited_target_follows_its_source_without_state():
    element = placed("app.subtitle", "Computed tomography viewer")
    assert children(element)[:2] == ["source", "target"]
    assert element.find("{*}target").text == "Computed tomography viewer"
    assert element.find("{*}target").get("state") is None


def test_a_cleared_target_is_removed():
    assert "target" not in children(placed("app.subtitle", ""))
