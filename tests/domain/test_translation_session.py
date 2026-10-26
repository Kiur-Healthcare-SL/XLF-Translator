from support.catalog_samples import catalog_with
from support.recorders import described

from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.language_pair import LanguagePair
from xlf_translator.domain.translation_session import TranslationSession
from xlf_translator.domain.unit_identifier import UnitIdentifier
from xlf_translator.domain.uploaded_document import UploadedDocument

SPANISH_TO_ENGLISH = LanguagePair(LanguageCode("es"), LanguageCode("en-GB"))


def session(catalog, languages=SPANISH_TO_ENGLISH):
    return TranslationSession.resumed(catalog, languages)


def ordinal(subject):
    return described(subject)["position"][0]


def test_resume_lands_on_the_first_untranslated_unit():
    assert ordinal(session(catalog_with(60, untranslated=[31, 38]))) == 31


def test_resume_passes_over_auto_filled_units():
    assert ordinal(session(catalog_with(60, auto_filled=[30], untranslated=[31]))) == 31


def test_resume_lands_on_an_imported_invalid_unit():
    assert ordinal(session(catalog_with(60, invalid=[44]))) == 44


def test_resume_lands_on_the_first_unit_when_all_are_translated():
    assert ordinal(session(catalog_with(60))) == 1


def test_movement_is_refused_in_both_directions_while_invalid():
    blocked = session(catalog_with(60, invalid=[44]))
    assert blocked.is_blocked()
    assert ordinal(blocked.forward()) == 44
    assert ordinal(blocked.backward()) == 44
    assert ordinal(blocked.jump(7)) == 44


def test_clearing_the_target_releases_the_block():
    cleared = session(catalog_with(60, invalid=[44])).enter_target(UnitIdentifier("unit.44"), "")
    assert not cleared.is_blocked()
    assert ordinal(cleared.forward()) == 45


def test_a_fresh_session_needs_a_target_language():
    fresh = session(catalog_with(3, default="untranslated"), LanguagePair(LanguageCode("es")))
    assert fresh.needs_target_language()
    assert not fresh.choose_target_language(LanguageCode("en-GB")).needs_target_language()


def test_copying_the_source_translates_the_current_unit():
    copied = session(catalog_with(3, untranslated=[2])).copy_source()
    assert copied.is_complete()


def test_exports_are_named_after_the_document_and_target_language():
    document = UploadedDocument("messages.xlf", b"")
    assert str(session(catalog_with(1)).draft_name(document)) == "messages.en-GB.draft.xlf"
    assert str(session(catalog_with(1)).final_name(document)) == "messages.en-GB.xlf"


def test_the_session_hands_its_catalog_and_language_to_a_writer():
    class Writer:
        def write(self, document, catalog, language):
            return f"{document} {catalog.size()} {language}".encode()

    document = UploadedDocument("messages.xlf", b"")
    assert session(catalog_with(3)).write_with(Writer(), document) == b"messages.xlf 3 en-GB"


def test_the_session_describes_itself():
    description = described(session(catalog_with(60, auto_filled=[30], untranslated=[31])))
    assert description["position"] == (31, 60)
    assert description["languages"] == ("es", "en-GB")
    assert description["classification"] == "partial"
    assert description["auto_filled"] == (30,)
    assert description["completion"] == ((31,), ())


def test_the_session_describes_its_current_unit():
    description = described(session(catalog_with(60, untranslated=[31])), "describe_current_into")
    assert description["identifier"] == "unit.31"
    assert description["position"] == (31, 60)
