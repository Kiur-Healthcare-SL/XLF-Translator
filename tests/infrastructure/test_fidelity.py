"""Writing keeps every element, attribute, text and comment the app did not edit."""

from xml.etree.ElementTree import Comment

import pytest
from support.fixture_documents import ALL, PARTIAL, fixture
from support.written_documents import NAMESPACE, parsed, trans_unit, written

TARGET = f"{NAMESPACE}target"
EDITS = {"app__title": "Edited", "viewer__limitedMode": "{2}x{1}", "status__ready": ""}


def shape(element):
    """Everything about an element and its descendants, targets and target-language aside."""
    attributes = {key: value for key, value in element.attrib.items() if key != "target-language"}
    kept = [child for child in element if child.tag != TARGET]
    return (element.tag, attributes, element.text, element.tail, [shape(child) for child in kept])


def untouched_targets(root, edited):
    targets = {}
    for unit in root.iter(f"{NAMESPACE}trans-unit"):
        if unit.get("id") not in edited and unit.find(TARGET) is not None:
            target = unit.find(TARGET)
            targets[unit.get("id")] = (target.attrib, target.text, [shape(child) for child in target])
    return targets


@pytest.mark.parametrize("name", ALL)
@pytest.mark.parametrize("edits", [{}, EDITS])
def test_everything_but_edited_targets_survives(name, edits):
    original = parsed(bytes(fixture(name)))
    output = parsed(written(name, **edits))
    assert shape(output) == shape(original)
    edited = {identifier.replace("__", ".") for identifier in edits} | {"layout.spacer"}
    assert untouched_targets(output, edited) == untouched_targets(original, edited)


@pytest.mark.parametrize("name", ALL)
def test_the_comment_survives_in_place(name):
    comments = [element.text for element in parsed(written(name, **EDITS)).iter() if element.tag is Comment]
    assert comments == [" Export and reporting screens "]


def test_an_untouched_target_keeps_its_state():
    target = trans_unit(parsed(written(PARTIAL)), "app.subtitle").find(TARGET)
    assert target.get("state") == "translated"


@pytest.mark.parametrize("name", ALL)
def test_the_default_namespace_is_kept_without_generated_prefixes(name):
    output = written(name, **EDITS)
    assert b'xmlns="urn:oasis:names:tc:xliff:document:1.2"' in output
    assert b"ns0" not in output
    assert b"xmlns:" not in output
