from xlf_translator.domain.document_size import DocumentSize


def test_exactly_four_mebibytes_is_within_the_limit():
    assert DocumentSize(4_194_304).is_within_limit()


def test_one_byte_more_is_over_the_limit():
    assert not DocumentSize(4_194_305).is_within_limit()


def test_the_refusal_states_the_limit_and_the_size_received():
    reason = str(DocumentSize(4_194_305).refusal())
    assert "4 MiB" in reason
    assert "4,194,305 bytes" in reason
