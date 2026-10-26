import re
from collections import Counter

from xlf_translator.domain.content import Content
from xlf_translator.domain.placeholder_token import PlaceholderToken

MASKED_TOKENS = re.compile(r"\{\{|\}\}|(\{[1-9][0-9]*\})")


class PlaceholderComparison:
    """Whether a masked target holds exactly the tokens of its source, and if not, why."""

    def __init__(self, source: Content, masked_target: str):
        self._source = source
        self._found = Counter(PlaceholderToken.parse(token) for token in MASKED_TOKENS.findall(masked_target) if token)

    def matches(self) -> bool:
        return self.problems() == ()

    def problems(self) -> tuple[str, ...]:
        return self._missing() + self._repeated() + self._unknown()

    def _expected(self) -> list[PlaceholderToken]:
        return [PlaceholderToken(number) for number in range(1, len(self._source.placeholders()) + 1)]

    def _markup(self, token: PlaceholderToken) -> str:
        return token.select_from(self._source.placeholders()).markup()

    def _missing(self) -> tuple[str, ...]:
        absent = [token for token in self._expected() if self._found[token] == 0]
        return tuple(f"{token} ({self._markup(token)}) is missing" for token in absent)

    def _repeated(self) -> tuple[str, ...]:
        repeated = [token for token in self._expected() if self._found[token] > 1]
        return tuple(f"{token} ({self._markup(token)}) is repeated" for token in repeated)

    def _unknown(self) -> tuple[str, ...]:
        unknown = sorted(token for token in self._found if token not in self._expected())
        return tuple(f"{token} is unknown" for token in unknown)
