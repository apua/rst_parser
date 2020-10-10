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
        while text and text[0] != '':
            yield text.pop(0)

    @classmethod
    def parse(cls, text):
        return cls(*text)


class LiteralBlock(Node):
    @classmethod
    def match(cls, text):
        if text and text[0] == '::':
            try:
                line = text[1]
            except IndexError:
                return True
            else:
                return line == '' or line.startswith(' ')
        else:
            return False

    @classmethod
    def fetch(cls, text):
        # remove colons
        colons = text.pop(0)
        assert colons == '::'

        if not text:
            print('WARN:LiteralBlock:EOF right after `::`')
            return

        # lstrip blank lines
        blanklines_before = False
        while text and text[0] == '':
            blanklines_before = True
            text.pop(0)
        if not blanklines_before:
            print('WARN:LiteralBlock:Blank line missing before literal block')

        indented = []
        while text \
                and (text[0].startswith(' ') or text[0] == ''):  # XXX: assume space only
            indented.append(text.pop(0))

        if not indented:
            print('WARN:LiteralBlock:None found')
            return

        # rstrip blank lines
        for idx in range(len(indented), 0, -1):
            if indented[idx-1] != '':
                break
        if text and idx == len(indented):
            print('WARN:LiteralBlock:Ends without a blank line')
        indented = indented[:idx]

        assert indented

        non_empty = filter(None, indented)
        len_leading_space = lambda s: len(s) - len(s.lstrip())
        len_indent = min(map(len_leading_space, non_empty))
        yield from (s[len_indent:] if s else '' for s in indented)

    @classmethod
    def parse(cls, text):
        return cls(*text)

    @staticmethod
    def patch_paragraph_fetch(fetch):
        import functools
        import re

        @functools.wraps(fetch)
        def fetch_(cls, text):
            buff = []
            for line in fetch(cls, text):
                buff.append(line)
                if text and text[0] != '' and text[0].startswith(' '):  # next line is indented
                    break

            if not buff:
                return

            last = buff.pop()
            if buff and last == '::':  # 'blah\n::'
                text.insert(0, '::')
                yield from buff
            elif m := re.search(r'^(.*?)(\s*)::$', last):  # 'blah::' or 'blah ::'
                text.insert(0, '::')
                yield from buff + [m.group(1) + ('' if m.group(2) else ':')]
            else:
                yield from buff + [last]

        return fetch_

Paragraph.fetch = classmethod(LiteralBlock.patch_paragraph_fetch(Paragraph.fetch.__func__))


class Document(Node):
    # XXX: require `match`, `fetch`, `parse` methods
    block_types = ['LiteralBlock', 'Paragraph']

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

    def insert(self, idx, v):
        self._buffer.insert(idx, v)
        self._is_empty = False
