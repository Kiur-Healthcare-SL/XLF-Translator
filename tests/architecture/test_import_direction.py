"""Dependencies point inwards: presentation -> application -> domain."""

import ast
from pathlib import Path

import pytest

PACKAGE_ROOT = Path(__file__).parents[2] / "src" / "xlf_translator"
XML_LIBRARIES = ("xml", "lxml", "defusedxml", "html.parser")
FORBIDDEN = {
    "domain": ("streamlit",) + XML_LIBRARIES + (
        "xlf_translator.application",
        "xlf_translator.infrastructure",
        "xlf_translator.presentation",
    ),
    "application": ("streamlit",) + XML_LIBRARIES + (
        "xlf_translator.infrastructure",
        "xlf_translator.presentation",
    ),
    "infrastructure": ("streamlit", "xlf_translator.presentation"),
}


def imported_modules(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            yield node.module


def violations(layer_directory, forbidden):
    found = []
    for path in sorted(layer_directory.rglob("*.py")):
        for module in imported_modules(path):
            if any(module == prefix or module.startswith(prefix + ".") for prefix in forbidden):
                found.append(f"{path.name} imports {module}")
    return found


@pytest.mark.parametrize("layer", sorted(FORBIDDEN))
def test_layer_imports_only_inwards(layer):
    assert violations(PACKAGE_ROOT / layer, FORBIDDEN[layer]) == []


@pytest.mark.parametrize(
    "statement",
    ["import streamlit", "from xml.etree import ElementTree", "from xlf_translator.application import x"],
)
def test_guard_reports_a_violating_domain_import(tmp_path, statement):
    (tmp_path / "offender.py").write_text(statement + "\n", encoding="utf-8")
    assert violations(tmp_path, FORBIDDEN["domain"]) != []
