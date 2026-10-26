from xlf_translator.presentation.whitespace_marker import WhitespaceMarker

MARKER = WhitespaceMarker()


def test_markup_in_a_source_renders_as_visible_text():
    marked = MARKER.mark("<p><b>Consejo</b></p>")
    assert "&lt;p&gt;&lt;b&gt;Consejo&lt;/b&gt;&lt;/p&gt;" in marked
    assert "<p>" not in marked


def test_leading_whitespace_is_marked():
    assert MARKER.mark("  Volver").startswith('<span class="edge-whitespace"')
    assert MARKER.mark("  Volver").endswith("</span>Volver")


def test_trailing_whitespace_is_marked():
    assert MARKER.mark("Serie: ").endswith(" </span>")


def test_inner_whitespace_is_not_marked():
    assert MARKER.mark("Corte axial") == "Corte axial"


def test_a_whitespace_only_source_is_marked_once():
    assert MARKER.mark("   ").count("<span") == 1


def test_a_block_keeps_whitespace_visible():
    assert "white-space: pre-wrap" in MARKER.block("a")
