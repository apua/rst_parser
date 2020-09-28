r"""
reStructuredText Parser

1.  Parse stateless line-based components
2.  During parsing line-based components,
    parse stateless inline components
3.  Calculate DOM to stateful
4.  Render from DOM
"""

from typing import List


class Node:
    r"""
    >>> Node(Node(1), Node('2', [3]), a=1)
    <Node {'a': 1}>
        <Node>
            1
        <Node>
            '2'
            [3]
    """
    def __init__(self, *nodes, **attrs): 
        self.nodes = nodes
        self.attrs = attrs

    def __str__(self):
        return repr(self)

    @property
    def tag(self) -> str:
        if self.attrs:
            return f'<{self.__class__.__name__} {self.attrs}>'
        else:
            return f'<{self.__class__.__name__}>'

    def reprlines(self) -> List[str]:
        indent = ' ' * 4
        yield self.tag
        for node in self.nodes:
            if isinstance(node, Node):
                yield from (f'{indent}{line}' for line in node.reprlines())
            else:
                yield f'{indent}{node!r}'

    def __repr__(self):
        return '\n'.join(self.reprlines())


class Document(Node): pass
class Paragraph(Node): pass


def parse_line_by_line(text):
    T = enumerate(text.splitlines())  # lazy
    buff = []
    for num, raw_line in T:
        line = raw_line.rstrip()
        if line:
            buff.append(line)
        else:
            yield Paragraph(*buff)
            buff.clear()

    if buff:
        yield Paragraph(*buff)


def parse(text):
    return Document(*parse_line_by_line(text))
            

sample_123 = (
    'blah blah blah blah\nblah blah blah blah   \n\n'
    'blah blah blah blah\t\n'
    )


dom_123 = Document(
    Paragraph('blah blah blah blah', 'blah blah blah blah'),
    Paragraph('blah blah blah blah'),
    )


def test_123():
    assert str(parse(sample_123)) == str(dom_123)
