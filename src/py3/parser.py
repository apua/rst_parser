# Internal Data Structure
# =======================

from dataclasses import dataclass, field

@dataclass
class Node:
    name: str
    attrs: dict = field(default_factory=dict)
    elems: list = field(default_factory=list)


def node(name):
    return lambda *elems: Node(name, elems=list(elems))


class Nodes:
    """
    >>> Nodes.document()
    Node(name='document', attrs={}, elems=[])
    >>> Nodes.document('a', 'b', 'c')
    Node(name='document', attrs={}, elems=['a', 'b', 'c'])
    """
    document = node('document')
    paragraph = node('paragraph')
    literal_block = node('literal_block')


# Parser Definitions
# ==================

class Parser:
    def parse(text):
        lines = list(map(str.rstrip, text.splitlines()))
        return Parser.document(lines, block_parsers=[Parser.blank, Parser.paragraph])

    def document(lines, block_parsers):
        document = Nodes.document()
        
        while lines:
            if __debug__: _number_lines = len(lines)
            for parser in block_parsers:
                if parser(lines, document):
                    break
            assert _number_lines > len(lines), (_number_lines, lines)

        return document

    def blank(lines, _):
        i = 0
        for line in lines:
            if line == '':
                i += 1
            else:
                break
        if i > 0:
            del lines[:i]
            return True
        else:
            return False

    def paragraph(lines, parent):
        i = 0
        for line in lines:
            if line:
                i += 1
            else:
                break

        if i > 0:
            parent.elems.append(Node('paragraph', elems=lines[:i]))
            del lines[:i]
            return True
        else:
            return False
