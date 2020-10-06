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
        def get_nonempty_lines(text):
            while text and text[0] != '':
                yield text.pop(0)

        return '\n'.join(get_nonempty_lines(text))

    @classmethod
    def parse(cls, text):
        return cls(text)


class Document(Node):
    # XXX: require `match`, `fetch`, `parse` methods
    block_types = ['Paragraph']

    @classmethod
    def parse(cls, text):
        block_types = tuple(map(globals().__getitem__, cls.block_types))

        def lstrip_empty_lines(text):
            while text and text[0] == '':
                text.pop(0)

        def _parse(text):
            while True:
                lstrip_empty_lines(text)
                if not text:
                    break

                node_type = next(node_type for node_type in block_types if node_type.match(text))
                yield node_type.parse(node_type.fetch(text))

        return cls(*_parse(text))


class BufferedText:
    r"""
    Provide `list`-like API for inline manipulation

    -   __bool__
    -   __getitem__
    -   clear
    -   pop
    """
    def __init__(self, text):
        self._lines = map(str.rstrip, text.splitlines())
        self._buffer = []
        self._is_empty = False

    def _readline(self):
        return self._buffer.append(next(self._lines))

    def __bool__(self):
        if self._buffer:
            return True

        if self._is_empty:
            return False

        try:
            self._readline()
        except StopIteration:
            self._is_empty = True
            return False
        else:
            return True

    def __getitem__(self, idx):
        if not (isinstance(idx, int) and idx >= 0):
            raise TypeError

        if self._is_empty:
            raise IndexError

        lack = idx + 1 - len(self._buffer)

        if lack <= 0:
            return self._buffer[idx]

        try:
            for i in range(lack):
                self._readline()
        except StopIteration:
            raise IndexError
        else:
            return self._buffer[idx]

    def clear(self):
        self._buffer.clear()
        self._is_empty = True

    def pop(self, idx):
        self[idx]  # ensure the value exists
        return self._buffer.pop(idx)
