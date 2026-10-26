from xlf_translator.domain.artifact_name import ArtifactName
from xlf_translator.domain.language_code import LanguageCode

ENGLISH = LanguageCode("en-GB")


def test_a_draft_is_named_after_stem_and_language():
    assert str(ArtifactName.draft("messages", ENGLISH)) == "messages.en-GB.draft.xlf"


def test_a_final_export_is_named_after_stem_and_language():
    assert str(ArtifactName.final("messages", ENGLISH)) == "messages.en-GB.xlf"


def test_a_stem_already_naming_the_language_is_not_repeated():
    assert str(ArtifactName.final("messages.fr", LanguageCode("fr"))) == "messages.fr.xlf"
    assert str(ArtifactName.draft("messages.en-GB", ENGLISH)) == "messages.en-GB.draft.xlf"


def test_a_stem_naming_another_language_is_kept():
    assert str(ArtifactName.final("messages.fr", ENGLISH)) == "messages.fr.en-GB.xlf"
