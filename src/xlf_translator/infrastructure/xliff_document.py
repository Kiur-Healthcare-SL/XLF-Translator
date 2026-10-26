from xml.etree.ElementTree import Element, ParseError, TreeBuilder, XMLParser


class XliffDocument:
    """Parses XLIFF bytes keeping comments, and names elements in the root's namespace."""

    def __init__(self, root: Element):
        self._root = root

    @staticmethod
    def parse(content: bytes) -> "XliffDocument | ParseError":
        parser = XMLParser(target=TreeBuilder(insert_comments=True))
        try:
            parser.feed(content)
            return XliffDocument(parser.close())
        except ParseError as error:
            return error

    def root(self) -> Element:
        return self._root

    def namespace(self) -> str:
        return self._root.tag[1:].split("}")[0] if self._root.tag.startswith("{") else ""

    def tag(self, local_name: str) -> str:
        namespace = self.namespace()
        return f"{{{namespace}}}{local_name}" if namespace else local_name

    @staticmethod
    def local_name(element: Element) -> str:
        return str(element.tag).rsplit("}", 1)[-1]
