# Internal Data Structure
# =======================

from dataclasses import dataclass, field

@dataclass
class Node:
    name: str
    attrs: dict = field(default_factory=dict)
    elems: list = field(default_factory=list)


# Parser Definitions
# ==================

from functools import wraps

def nonemtpy_input(func):
    @wraps(func)
    def func_(lines, *a, **kw):
        assert lines
        return func(lines, *a, **kw)
    return func_


class Parser:
    def parse(text):
        lines = [line.rstrip().replace('\t', ' '*4) for line in text.splitlines()]
        return Parser.document(lines, block_parsers=[
            Parser.blank,
            Parser.literal_block,
            #Parser.paragraph,
            Parser.paragraph_chain_literal,
            ])

    def document(lines, block_parsers):
        document_node = Node('document')

        while lines:
            if __debug__:
                _number_lines = len(lines)

            for parse in block_parsers:
                if (result := parse(lines)) is not None:
                    offset, elems = result
                    del lines[:offset]
                    document_node.elems += elems
                    break

            assert _number_lines > len(lines), (_number_lines, lines)

        return document_node

    @nonemtpy_input
    def blank(lines):
        offset = 0
        for line in lines:
            if line == '':
                offset += 1
            else:
                break

        if offset > 0:
            return offset, ()

    @nonemtpy_input
    def paragraph(lines):
        offset = 0
        for line in lines:
            if line != '':
                offset += 1
            else:
                break

        if offset > 0:
            return offset, [Node('paragraph', elems=lines[:offset])]

    @nonemtpy_input
    def paragraph_chain_literal(lines):
        offset = 0
        literal_result = None
        for line in lines:
            if line != '':
                offset += 1
            else:
                break

            if line.endswith('::') and (literal_result := Parser.literal_block(['::'] + lines[offset:])) is not None:
                break

        if offset > 0:
            if literal_result is None:
                paragraph_lines = lines[:offset]
                paragraph_node = Node('paragraph', elems=paragraph_lines)
                return offset, [paragraph_node]
            else:
                lastline = lines[offset-1]
                trailing_colon = '' if lastline.endswith(' ::') else ':'
                paragraph_lines = lines[:offset-1] + [lastline[:-2].rstrip() + trailing_colon]
                nodes = [Node('paragraph', elems=paragraph_lines)]

                literal_offset, literal_nodes = literal_result
                offset = offset - 1 + literal_offset
                nodes += literal_nodes

                return offset, nodes

    @nonemtpy_input
    def literal_block(lines):
        if lines[0] == '::':
            if len(lines) == 1:  # EOF
                return 1, ()
            elif lines[1] == '' or lines[1].startswith(' '):
                pass
            else:
                return
        else:
            return

        offset = 1
        for line in lines[offset:]:
            if line == '':
                offset += 1
            else:
                break
        blank_before = offset > 1

        indented = [line for line in lines[offset:] if line == '' or line.startswith(' ')]
        offset += len(indented)

        if not indented:
            return offset, ()

        width = min(len(s) - len(s.lstrip()) for s in indented if s != '')
        dedented = [s if s == '' else s[width:] for s in indented]

        i = len(dedented)
        for line in reversed(dedented):
            if line == '':
                i -= 1
        del dedented[i:]

        return offset, [Node('literal_block', elems=dedented)]
