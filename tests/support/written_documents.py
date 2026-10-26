"""Writing fixture catalogs back out, and looking inside the result."""

from xml.etree.ElementTree import TreeBuilder, XMLParser

from support.fixture_documents import fixture, read

from xlf_translator.domain.language_code import LanguageCode
from xlf_translator.domain.unit_identifier import UnitIdentifier
from xlf_translator.infrastructure.element_tree_catalog_writer import ElementTreeCatalogWriter

NAMESPACE = "{urn:oasis:names:tc:xliff:document:1.2}"


def written(name, language="en-GB", **targets):
    catalog, _ = read(name)
    for identifier, masked in targets.items():
        catalog = catalog.with_target(UnitIdentifier(identifier.replace("__", ".")), masked)
    return ElementTreeCatalogWriter().write(fixture(name), catalog, LanguageCode(language))


def parsed(content):
    parser = XMLParser(target=TreeBuilder(insert_comments=True))
    parser.feed(content)
    return parser.close()


def trans_unit(root, identifier):
    return root.find(f".//{NAMESPACE}trans-unit[@id='{identifier}']")


def children(unit):
    return [child.tag.replace(NAMESPACE, "") for child in unit]
