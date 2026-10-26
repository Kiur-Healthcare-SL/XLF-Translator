from xlf_translator.infrastructure.encoding_check import EncodingCheck


def test_a_utf_8_document_passes():
    assert EncodingCheck('<?xml version="1.0" encoding="UTF-8"?><a>ñ</a>'.encode()).refusal() is None


def test_a_document_without_declaration_passes():
    assert EncodingCheck(b"<a/>").refusal() is None


def test_a_byte_order_mark_is_accepted():
    assert EncodingCheck(b'\xef\xbb\xbf<?xml version="1.0" encoding="utf-8"?><a/>').refusal() is None


def test_another_declared_encoding_is_refused_naming_both():
    reason = str(EncodingCheck(b'<?xml version="1.0" encoding="ISO-8859-1"?><a/>').refusal())
    assert "UTF-8" in reason
    assert "ISO-8859-1" in reason


def test_invalid_utf_8_bytes_are_refused():
    reason = str(EncodingCheck(b"<a>\xe9</a>").refusal())
    assert "UTF-8" in reason
    assert "byte 3" in reason
