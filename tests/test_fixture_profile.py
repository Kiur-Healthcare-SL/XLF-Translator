"""The three fixture catalogs follow the profile of design D14.

Standard library only, so the fixtures are checked independently of the code
under test.
"""

from pathlib import Path
from xml.etree.ElementTree import Comment, TreeBuilder, XMLParser

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
NAMESPACE = "{urn:oasis:names:tc:xliff:document:1.2}"
FRESH = "messages.xlf"
PARTIAL = "messages.en-GB.xlf"
COMPLETED = "messages.fr.xlf"
ALL = (FRESH, PARTIAL, COMPLETED)
NON_BREAKING_SPACE = " "
FOUR_MEBIBYTES = 4 * 1024 * 1024


def parse(name):
    parser = XMLParser(target=TreeBuilder(insert_comments=True))
    parser.feed((FIXTURES / name).read_bytes())
    return parser.close()


def units(name):
    return list(parse(name).iter(f"{NAMESPACE}trans-unit"))


def text_of(element):
    return "".join(element.itertext())


def content_of(element):
    """Text with each placeholder standing as one object replacement character."""
    pieces = [element.text or ""]
    pieces += ["\ufffc" + (child.tail or "") for child in element]
    return "".join(pieces)


def placeholders(element):
    return element.findall(f"{NAMESPACE}x")


def source(unit):
    return unit.find(f"{NAMESPACE}source")


def target(unit):
    return unit.find(f"{NAMESPACE}target")


def ordinals_where(name, predicate):
    return [ordinal for ordinal, unit in enumerate(units(name), start=1) if predicate(unit)]


def is_whitespace_only(text):
    return text != "" and text.strip() == ""


@pytest.mark.parametrize("name", ALL)
def test_every_fixture_has_sixty_units(name):
    assert len(units(name)) == 60


@pytest.mark.parametrize("name", ALL)
def test_every_fixture_shares_identifiers_and_order(name):
    identifiers = [unit.get("id") for unit in units(name)]
    assert identifiers == [unit.get("id") for unit in units(FRESH)]


@pytest.mark.parametrize("name", ALL)
def test_every_fixture_is_under_four_mebibytes(name):
    assert (FIXTURES / name).stat().st_size < FOUR_MEBIBYTES


@pytest.mark.parametrize("name", ALL)
def test_every_unit_carries_a_location_context_group(name):
    groups = [unit.find(f"{NAMESPACE}context-group[@purpose='location']") for unit in units(name)]
    assert all(group is not None for group in groups)


@pytest.mark.parametrize("name", ALL)
def test_about_twenty_units_carry_notes(name):
    with_notes = ordinals_where(name, lambda unit: unit.find(f"{NAMESPACE}note") is not None)
    assert 18 <= len(with_notes) <= 22


@pytest.mark.parametrize("name", ALL)
def test_one_comment_is_present(name):
    comments = [element for element in parse(name).iter() if element.tag is Comment]
    assert len(comments) == 1


def test_fresh_declares_spanish_source_and_no_target_language():
    file_element = parse(FRESH).find(f"{NAMESPACE}file")
    assert file_element.get("source-language") == "es"
    assert file_element.get("target-language") is None


def test_fresh_has_no_targets():
    assert ordinals_where(FRESH, lambda unit: target(unit) is not None) == []


def test_fresh_placeholder_profile():
    with_placeholders = ordinals_where(FRESH, lambda unit: placeholders(source(unit)))
    assert len(with_placeholders) == 8
    assert {44, 52} <= set(with_placeholders)
    counts = [len(placeholders(source(unit))) for unit in units(FRESH)]
    assert max(counts) == 10


def test_fresh_has_a_repeated_placeholder_identifier():
    def repeats(unit):
        identifiers = [element.get("id") for element in placeholders(source(unit))]
        return len(identifiers) != len(set(identifiers))

    assert len(ordinals_where(FRESH, repeats)) >= 1


def test_fresh_has_interpolation_and_button_wrapping_an_icon():
    def identifiers(unit):
        return [element.get("id") for element in placeholders(source(unit))]

    assert ordinals_where(FRESH, lambda unit: "INTERPOLATION" in identifiers(unit))
    wrapping = ordinals_where(
        FRESH, lambda unit: identifiers(unit)[:2] == ["START_TAG_BUTTON", "START_TAG_MAT_ICON"]
    )
    assert len(wrapping) == 1


def test_fresh_whitespace_profile():
    def padded(unit):
        text = content_of(source(unit))
        return text.strip() != "" and text != text.strip()

    def non_breaking(unit):
        text = content_of(source(unit))
        return padded(unit) and (text[0] == NON_BREAKING_SPACE or text[-1] == NON_BREAKING_SPACE)

    assert len(ordinals_where(FRESH, padded)) == 6
    assert len(ordinals_where(FRESH, non_breaking)) == 2
    assert ordinals_where(FRESH, lambda unit: is_whitespace_only(text_of(source(unit)))) == [30]


def test_fresh_escaped_html_profile():
    with_markup = [text_of(source(unit)) for unit in units(FRESH) if "<" in text_of(source(unit))]
    assert len(with_markup) == 3
    assert max(len(text) for text in with_markup) > 800


def test_fresh_has_one_unit_with_literal_braces():
    assert len(ordinals_where(FRESH, lambda unit: "{" in text_of(source(unit)))) == 1


def test_partial_declares_english_target_language():
    assert parse(PARTIAL).find(f"{NAMESPACE}file").get("target-language") == "en-GB"


def test_partial_target_gaps_and_damage():
    assert ordinals_where(PARTIAL, lambda unit: target(unit) is None) == [30, 31]
    blank = ordinals_where(
        PARTIAL, lambda unit: target(unit) is not None and is_whitespace_only(text_of(target(unit)))
    )
    assert blank == [38]
    stripped = ordinals_where(
        PARTIAL,
        lambda unit: placeholders(source(unit)) and target(unit) is not None and not placeholders(target(unit)),
    )
    assert stripped == [44, 52]


def test_partial_identical_targets_and_state():
    identical = ordinals_where(
        PARTIAL, lambda unit: target(unit) is not None and text_of(target(unit)) == text_of(source(unit))
    )
    assert len(identical) == 4
    stated = ordinals_where(PARTIAL, lambda unit: target(unit) is not None and target(unit).get("state"))
    assert len(stated) == 1


def test_completed_declares_french_and_lacks_only_unit_thirty():
    assert parse(COMPLETED).find(f"{NAMESPACE}file").get("target-language") == "fr"
    assert ordinals_where(COMPLETED, lambda unit: target(unit) is None) == [30]


def test_completed_targets_keep_their_source_placeholders():
    def same_placeholders(unit):
        def names(element):
            return sorted(child.get("id") for child in placeholders(element))

        return target(unit) is None or names(source(unit)) == names(target(unit))

    assert all(same_placeholders(unit) for unit in units(COMPLETED))

