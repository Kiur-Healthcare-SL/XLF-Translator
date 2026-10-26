from xml.etree.ElementTree import Comment, ParseError

from xlf_translator.infrastructure.xliff_document import XliffDocument

NAMESPACE = "urn:oasis:names:tc:xliff:document:1.2"


def test_a_namespaced_document_names_tags_in_its_namespace():
    xliff = XliffDocument.parse(f'<xliff xmlns="{NAMESPACE}"><file/></xliff>'.encode())
    assert xliff.namespace() == NAMESPACE
    assert xliff.root().find(xliff.tag("file")) is not None


def test_a_document_without_namespace_uses_plain_tags():
    assert XliffDocument.parse(b"<xliff/>").tag("file") == "file"


def test_comments_are_kept():
    xliff = XliffDocument.parse(b"<xliff><!-- note --></xliff>")
    assert [child.tag for child in xliff.root()] == [Comment]


def test_malformed_xml_yields_the_parse_error():
    assert isinstance(XliffDocument.parse(b"<xliff>"), ParseError)


def test_local_names_drop_the_namespace():
    xliff = XliffDocument.parse(f'<xliff xmlns="{NAMESPACE}"/>'.encode())
    assert XliffDocument.local_name(xliff.root()) == "xliff"
