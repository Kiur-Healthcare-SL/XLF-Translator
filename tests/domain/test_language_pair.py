from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.language_pair import LanguagePair


class LanguageRecorder:
    def languages(self, source, target):
        self.described = (source, target)


def described(pair):
    recorder = LanguageRecorder()
    pair.describe_into(recorder)
    return recorder.described


def test_a_pair_may_have_a_source_and_no_target():
    pair = LanguagePair(LanguageCode("es"))
    assert not pair.has_target()
    assert described(pair) == ("es", None)


def test_a_pair_adopts_a_target():
    pair = LanguagePair(LanguageCode("es")).adopt_target(LanguageCode("en-GB"))
    assert pair.has_target()
    assert described(pair) == ("es", "en-GB")
    assert pair == LanguagePair(LanguageCode("es"), LanguageCode("en-GB"))


def test_adopting_leaves_the_original_pair_unchanged():
    pair = LanguagePair(LanguageCode("es"))
    pair.adopt_target(LanguageCode("fr"))
    assert not pair.has_target()


def test_a_pair_names_exports_with_its_target():
    from xlf_translator.domain.uploaded_document import UploadedDocument

    pair = LanguagePair(LanguageCode("es"), LanguageCode("fr"))
    document = UploadedDocument("messages.xlf", b"")
    assert str(pair.draft_name(document)) == "messages.fr.draft.xlf"
    assert str(pair.final_name(document)) == "messages.fr.xlf"
