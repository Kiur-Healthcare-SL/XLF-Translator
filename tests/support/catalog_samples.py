"""Units and catalogs in known states, shared by domain and application tests."""

from support.content_samples import BOLD_PHRASE

from xlf_translator.domain.catalog import Catalog
from xlf_translator.domain.content import Content
from xlf_translator.domain.translation_unit import TranslationUnit
from xlf_translator.domain.unit_identifier import UnitIdentifier

TRANSLATED = "translated"
UNTRANSLATED = "untranslated"
INVALID = "invalid"
AUTO_FILLED = "auto-filled"


def unit(ordinal, state):
    identifier = UnitIdentifier(f"unit.{ordinal}")
    if state == AUTO_FILLED:
        return TranslationUnit.parsed(identifier, Content.of_text("   "), None)
    source = TranslationUnit.parsed(identifier, BOLD_PHRASE, None)
    targets = {TRANSLATED: "{1}done{2}", UNTRANSLATED: "", INVALID: "{1}damaged"}
    return source.with_target(targets[state])


def catalog(*states):
    return Catalog(unit(ordinal, state) for ordinal, state in enumerate(states, start=1))


def catalog_with(size, default=TRANSLATED, **exceptions):
    """`catalog_with(60, untranslated=[31], invalid=[44])`."""
    by_ordinal = {ordinal: state.replace("_", "-") for state, ordinals in exceptions.items() for ordinal in ordinals}
    return catalog(*(by_ordinal.get(ordinal, default) for ordinal in range(1, size + 1)))
