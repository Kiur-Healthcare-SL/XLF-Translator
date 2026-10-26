from xml.etree.ElementTree import Element, SubElement


class ContentIntoElement:
    """Writes content into an empty element: text runs as text, placeholders as `<x/>`."""

    def __init__(self, element: Element, placeholder_tag: str):
        self._element = element
        self._placeholder_tag = placeholder_tag

    def text(self, text: str) -> None:
        children = list(self._element)
        if children:
            children[-1].tail = (children[-1].tail or "") + text
            return
        self._element.text = (self._element.text or "") + text

    def placeholder(self, attributes: tuple[tuple[str, str], ...]) -> None:
        SubElement(self._element, self._placeholder_tag, dict(attributes))
