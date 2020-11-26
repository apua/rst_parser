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

class Configurable: pass

class NodeParser(Configurable, NodeLogger, NodeRepresentation, GenericFuncCall): pass

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
