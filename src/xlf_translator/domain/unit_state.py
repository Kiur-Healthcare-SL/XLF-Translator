from enum import Enum


class UnitState(Enum):
    """Where a translation unit stands; see design D13."""

    TRANSLATED = "translated"
    UNTRANSLATED = "untranslated"
    INVALID = "invalid"
