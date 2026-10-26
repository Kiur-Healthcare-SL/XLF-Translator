import re

from xlf_translator.domain.catalog_refusal import CatalogRefusal

BYTE_ORDER_MARK = b"\xef\xbb\xbf"
DECLARED_ENCODING = re.compile(rb"""^<\?xml[^>]*?encoding\s*=\s*["']([^"']+)["']""")
UTF_8_NAMES = {"utf-8", "utf8"}


class EncodingCheck:
    """Refuses documents not encoded as UTF-8, before they are parsed (design D12).

    A UTF-8 byte order mark is accepted for now; see note N4.
    """

    def __init__(self, content: bytes):
        self._content = content.removeprefix(BYTE_ORDER_MARK)

    def refusal(self) -> CatalogRefusal | None:
        return self._declaration_refusal() or self._byte_refusal()

    def _declaration_refusal(self) -> CatalogRefusal | None:
        declared = DECLARED_ENCODING.match(self._content)
        if declared is None or declared.group(1).decode("ascii", "replace").lower() in UTF_8_NAMES:
            return None
        return CatalogRefusal("encoding UTF-8", f"encoding {declared.group(1).decode('ascii', 'replace')}")

    def _byte_refusal(self) -> CatalogRefusal | None:
        try:
            self._content.decode("utf-8")
            return None
        except UnicodeDecodeError as error:
            return CatalogRefusal("UTF-8 encoded content", f"an invalid UTF-8 byte sequence at byte {error.start}")
