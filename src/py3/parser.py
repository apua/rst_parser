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

from functools import wraps

def nonemtpy_input(func):
    @wraps(func)
    def func_(lines, *a, **kw):
        assert lines
        return func(lines, *a, **kw)
    return func_


class Parser:
    def parse(text):
        lines = list(map(str.rstrip, text.splitlines()))
        return Parser.document(lines, block_parsers=[
            Parser.blank,
            Parser.literal_block,
            Parser.paragraph,
            ])

    def document(lines, block_parsers):
        document = Nodes.document()

        while lines:
            if __debug__: _number_lines = len(lines)
            print('turn start', lines)
            for parse in block_parsers:
                print('parse ->', parse.__name__, lines)
                result = parse(lines, document)
                if result is not None:
                    offset, elems = result
                    del lines[:offset]
                    document.elems.extend(elems)
                    break
            #for parser in block_parsers:
            #    if parser(lines, document):
            #        break
            print('turn end', lines)
            assert _number_lines > len(lines), (_number_lines, lines)

        return document

    @nonemtpy_input
    def blank(lines, parent=None):
        if lines[0] != '':
            return False


        for i, line in enumerate(lines):
            if line != '':
                break
        else:
            i += 1
        del lines[:i]
        return True

    @nonemtpy_input
    def blank(lines, parent=None):
        offset = 0
        for line in lines:
            if line == '':
                offset += 1
            else:
                break

        if offset > 0:
            return offset, ()

    @nonemtpy_input
    def paragraph_plain(lines, parent):
        if lines[0] == '':
            return False

        for i, line in enumerate(lines):
            if line == '':
                break
        else:
            i += 1
        parent.elems.append(Node('paragraph', elems=lines[:i]))
        del lines[:i]
        return True

    @nonemtpy_input
    def paragraph(lines, parent):
        return Parser.paragraph_plain(lines, parent)

    @nonemtpy_input
    def paragraph(lines, parent):
        offset = 0
        for line in lines:
            if line != '':
                offset += 1
            else:
                break

        if offset > 0:
            return offset, [Node('paragraph', elems=lines[:offset])]

    @nonemtpy_input
    def literal_block(lines, parent):
        if lines[0] != '::':
            return False

        if len(lines) == 1:  # EOF
            # system_message warning "Literal block expected; none found."
            del lines[0]
            return True

        follow_literal_context = lines[1] == '' or lines[1].startswith(' ')
        if not follow_literal_context:
            return False

        del lines[0]
        blank_before = Parser.blank(lines)
        indented = [line for line in lines if line == '' or line.startswith(' ')]

        if blank_before and not indented:
            # system_message warning "Literal block expected; none found."
            if not lines:  # EOF
                return True
            else:
                return False

        if not blank_before and indented:
            pass  # system_message error "Unexpected indentation."

        ...
        assert False
        return True

    @nonemtpy_input
    def literal_block(lines, parent):
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

        print(f'{blank_before=}, {indented=}')

        if not indented:
            return offset, ()

        width = min(len(s) - len(s.lstrip()) for s in indented if s != '')
        dedented = [s if s == '' else s[width:] for s in indented]

        print(f'-----> {dedented=}')

        i = len(dedented)
        for line in reversed(dedented):
            if line == '':
                i -= 1
        del dedented[i:]

        return offset, [Node('literal_block', elems=dedented)]
