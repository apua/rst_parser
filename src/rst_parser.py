r"""
reStructuredText Parser

1.  Parse stateless line-based components
2.  During parsing line-based components,
    parse stateless inline components
3.  Calculate DOM to stateful
4.  Render from DOM
"""

# XXX: consider "given full text, output DOM" only,
#      no more requirement like "iter (lazy) DOM" or "partial text modification"

# XXX: "parsing inline w/o given block type" is unreasonable

# XXX: "the end of block" condition always provided

# XXX: processing text line by line with state machine and buffer
#      makes it hard to maintain due to implicit state changes;
#      I would like replace state machine with call stack,
#      and wrap text reading with buffer
#      where the wrapped text can be debugable

# XXX: each node type inherit `Node` for data structure
#      and bind related methods under the namespace

from data_structure import Node


class Paragraph(Node):
    inline_types = []

    @classmethod
    def match(cls, text):
        return True

    @classmethod
    def fetch(cls, text):
        return '\n'.join(text.get_nonempty_lines())

    @classmethod
    def build(cls, text):
        return cls(text)


class Document(Node):
    # XXX: require `match`, `fetch`, `build` methods
    block_types = ['Paragraph']

    @classmethod
    def build(cls, text):
        block_types = tuple(map(globals().__getitem__, cls.block_types))

        def parse(text):
            while True:
                text.lstrip_empty_lines()
                if text.is_empty:
                    break

                node_type = next(node_type for node_type in block_types if node_type.match(text))
                yield node_type.build(node_type.fetch(text))

        return cls(*parse(text))


class BufferedText:
    def __init__(self, text):
        self.lines = map(str.rstrip, text.splitlines())
        self.buffer = []
        self._is_empty = False

    def __bool__(self):
        return not self.is_empty

    @property
    def is_empty(self):
        if self._is_empty:
            return True

        if not self.buffer:
            try:
                self.buffer.append(next(self.lines))
            except StopIteration:
                return True

        return False

    def lstrip_empty_lines(self):
        while self.buffer:
            if self.buffer[0] == '':
                self.buffer.pop(0)

        for line in self.lines:
            if line != '':
                self.buffer.append(line)
                break
        else:
            self._is_empty = True

    def get_nonempty_lines(self):
        while self.buffer:
            line = self.buffer.pop(0)
            if line:
                yield line
            else:
                return

        for line in self.lines:
            if line:
                yield line
            else:
                self.buffer.append(line)
                return

def parse(text):
    text = BufferedText(text)
    return Document.build(text)


sample_123 = (
    'blah blah blah blah\n'
    'blah blah blah blah   \n'
    '\n'
    'blah blah blah blah\t\n'
    )


dom_123 = Document(
    Paragraph('blah blah blah blah\nblah blah blah blah'),
    Paragraph('blah blah blah blah'),
    )


def test_123():
    assert str(parse(sample_123)) == str(dom_123)
