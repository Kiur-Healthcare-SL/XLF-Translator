"""Hard limits from AGENTS.md, checked over the whole source tree."""

import ast
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[2]
PACKAGE_ROOT = PROJECT_ROOT / "src" / "xlf_translator"
TESTS_ROOT = PROJECT_ROOT / "tests"
FUNCTION_LIMIT = 20
CLASS_LIMIT = 200


def source_files(root):
    return [path for path in sorted(root.rglob("*.py")) if path.name != "__init__.py"]


def length(node):
    return node.end_lineno - node.lineno + 1


def snake_case(name):
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def limit_violations(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and length(node) >= FUNCTION_LIMIT:
            found.append(f"{path.name}: function {node.name} has {length(node)} lines")
        if isinstance(node, ast.ClassDef) and length(node) >= CLASS_LIMIT:
            found.append(f"{path.name}: class {node.name} has {length(node)} lines")
    return found


def top_level_classes(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [node.name for node in tree.body if isinstance(node, ast.ClassDef)]


def file_violations(path):
    classes = top_level_classes(path)
    if len(classes) > 1:
        return [f"{path.name}: holds {len(classes)} classes"]
    if classes and snake_case(classes[0]) != path.stem:
        return [f"{path.name}: holds class {classes[0]}"]
    return []


def all_violations(root):
    found = []
    for path in source_files(root):
        found += limit_violations(path) + file_violations(path)
    return found


def test_source_tree_respects_limits():
    assert all_violations(PACKAGE_ROOT) == []


def test_every_class_has_a_mirrored_test_file():
    missing = []
    for path in source_files(PACKAGE_ROOT):
        relative = path.relative_to(PACKAGE_ROOT)
        expected = TESTS_ROOT / relative.parent / f"test_{relative.name}"
        if top_level_classes(path) and not expected.exists():
            missing.append(str(relative))
    assert missing == []


def test_limits_report_an_oversized_sample(tmp_path):
    body = "\n".join(f"    value_{index} = {index}" for index in range(25))
    (tmp_path / "sample.py").write_text(f"def oversized():\n{body}\n", encoding="utf-8")
    assert all_violations(tmp_path) == ["sample.py: function oversized has 26 lines"]


def test_limits_report_two_classes_in_one_file(tmp_path):
    (tmp_path / "first.py").write_text("class First:\n    pass\n\n\nclass Second:\n    pass\n", encoding="utf-8")
    assert all_violations(tmp_path) == ["first.py: holds 2 classes"]


def test_limits_report_a_file_not_named_after_its_class(tmp_path):
    (tmp_path / "wrong.py").write_text("class UnitIdentifier:\n    pass\n", encoding="utf-8")
    assert all_violations(tmp_path) == ["wrong.py: holds class UnitIdentifier"]
