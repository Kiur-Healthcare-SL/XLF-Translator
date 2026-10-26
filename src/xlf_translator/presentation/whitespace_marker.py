import html
import re

EDGE_WHITESPACE = re.compile(r"^\s+|\s+$")
MARKED = '<span class="edge-whitespace" style="text-decoration: underline wavy red; background: rgba(255, 0, 0, 0.15)">{}</span>'


class WhitespaceMarker:
    """Renders text as HTML with leading and trailing whitespace marked (design D7).

    The text is escaped first, so markup in a source shows as the characters
    it is, never as live HTML.
    """

    def mark(self, text: str) -> str:
        return EDGE_WHITESPACE.sub(lambda match: MARKED.format(match.group(0)), html.escape(text))

    def block(self, text: str) -> str:
        return f'<div style="white-space: pre-wrap; font-family: monospace">{self.mark(text)}</div>'
