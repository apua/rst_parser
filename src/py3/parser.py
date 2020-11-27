# Internal Data Structure
# =======================

from dataclasses import dataclass, field

@dataclass
class Node:
    name: str
    attrs: dict = field(default_factory=dict)
    elems: list = field(default_factory=list)


# Base Parser
# ===========

class NodeLogger: pass

class NodeRepresentation: pass

class GenericFuncCall:
    def __call__(self, *a, **kw):
        return Node(self.name, *a, **kw)


from dataclasses import dataclass

@dataclass
class Configure:
    blocks: list = None
    inlines: list = None


class NodeParser(Configure, NodeLogger, NodeRepresentation, GenericFuncCall):
    @property
    def name(self):
        return self.__class__.__name__.lower()


# Parser Definitions
# ==================

class Document(NodeParser):
    def remove_leading_blanks(self, lines):
        while lines:
            if lines[0] == '':
                del lines[0]

    def parse(self, text):
        node = Node(self.name)
        lines = list(map(str.rstrip, text.splitlines()))

        while True:
            self.remove_leading_blanks(lines)
            if not lines:
                break

        return node


class Paragraph(NodeParser):
    pass


# Configuration
# =============

paragraph = Paragraph()
document = Document(blocks=[paragraph])


# Export
# ======

def parse(text) -> Node:
    return document.parse(text)


__all__ = [
    'Node',
    'parse',
    'document',
    'paragraph',
    ]
