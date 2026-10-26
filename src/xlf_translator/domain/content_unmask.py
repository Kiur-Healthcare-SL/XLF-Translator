import re

from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder import Placeholder
from xlf_translator.domain.placeholder_token import PlaceholderToken
from xlf_translator.domain.text_run import TextRun

MASKED_PIECES = re.compile(r"(\{\{|\}\}|\{[1-9][0-9]*\})")
BRACE_ESCAPES = {"{{": "{", "}}": "}"}


class ContentUnmask:
    """Restores masked text to content, each `{n}` becoming the source's n-th placeholder.

    Tokens may appear in any order. A token the source does not number, and a
    lone brace, stay literal text.
    """

    def __init__(self, source: Content):
        self._reference = source.placeholders()

    def unmask(self, masked: str) -> Content:
        return Content(self._restored(piece) for piece in MASKED_PIECES.split(masked) if piece)

    def _restored(self, piece: str) -> TextRun | Placeholder:
        if piece in BRACE_ESCAPES:
            return TextRun(BRACE_ESCAPES[piece])
        token = PlaceholderToken.parse(piece)
        return (token and token.select_from(self._reference)) or TextRun(piece)
