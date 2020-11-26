# Internal Data Structure
# =======================

from dataclasses import dataclass, field

@dataclass
class Node:
    name: str
    attrs: dict = field(default_factory=dict)
    elems: list = field(default_factory=list)


# Definitions
# ===========

class NodeLogger: pass

class NodeRepresentation: pass

class GenericFuncCall: pass

from dataclasses import dataclass

@dataclass
class Configurable:
    blocks: list = None
    inlines: list = None

    def __post_init__(self):
        assert any([self.blocks, self.inlines])

class NodeParser(Configurable, NodeLogger, NodeRepresentation, GenericFuncCall):
    @property
    def name(self):
        return self.__class__.__name__.lower()

    def __call__(self, attrs=None, elems=None):
        return Node(self.name)

class Document(NodeParser):
    pass

class Paragraph(NodeParser):
    pass


# Configuration
# =============

paragraph = Paragraph()
document = Document()


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
