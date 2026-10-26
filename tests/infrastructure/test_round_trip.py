"""Masking and writing lose nothing, over every fixture unit."""

import pytest
from support.fixture_documents import ALL, FIXTURES, fixture, read
from support.written_documents import NAMESPACE, parsed

from xlf_translator.domain.content_mask import ContentMask
from xlf_translator.domain.content_unmask import ContentUnmask
from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.uploaded_document import UploadedDocument
from xlf_translator.infrastructure.content_from_element import ContentFromElement
from xlf_translator.infrastructure.element_tree_catalog_reader import ElementTreeCatalogReader
from xlf_translator.infrastructure.element_tree_catalog_writer import ElementTreeCatalogWriter


def contents(name):
    for unit in parsed((FIXTURES / name).read_bytes()).iter(f"{NAMESPACE}trans-unit"):
        source = ContentFromElement(unit.find(f"{NAMESPACE}source")).content()
        elements = [unit.find(f"{NAMESPACE}source"), unit.find(f"{NAMESPACE}target")]
        yield from ((source, ContentFromElement(element).content()) for element in elements if element is not None)


@pytest.mark.parametrize("name", ALL)
def test_unmasking_the_mask_of_every_source_and_target_gives_it_back(name):
    pairs = list(contents(name))
    assert len(pairs) >= 60
    for source, content in pairs:
        assert ContentUnmask(source).unmask(ContentMask(source).mask(content)) == content


@pytest.mark.parametrize("name", ALL)
@pytest.mark.parametrize("language", ["en-GB", "fr"])
def test_writer_output_re_parses_to_an_equal_catalog(name, language):
    catalog, languages = read(name)
    output = ElementTreeCatalogWriter().write(fixture(name), catalog, LanguageCode(language))
    reread_catalog, reread_languages = ElementTreeCatalogReader().read(UploadedDocument(name, output))
    assert reread_catalog == catalog
    assert reread_languages == languages.adopt_target(LanguageCode(language))
