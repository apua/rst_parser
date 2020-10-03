"""
document:

#. block_quote
#. bullet_list
#. enumerated_list
#. field_list
       [x] docinfo (bibliography and RCS keywords)
#. [x] option_list
#. doctest_block
#. line_block
#. table (grid / simple)
#. explicit markup block
       (footnote, citation, hyperlink target, anonymous, directive, substitution, comment)
#. transition

#. section title
#. definition_list
#. paragraph
#. literal_block
"""


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
    def parse(cls, text):
        return cls(text)


class Document(Node):
    # XXX: require `match`, `fetch`, `parse` methods
    block_types = ['Paragraph']

    @classmethod
    def parse(cls, text):
        block_types = tuple(map(globals().__getitem__, cls.block_types))

        def _parse(text):
            while True:
                text.lstrip_empty_lines()
                if text.is_empty:
                    break

                node_type = next(node_type for node_type in block_types if node_type.match(text))
                yield node_type.parse(node_type.fetch(text))

        return cls(*_parse(text))


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
