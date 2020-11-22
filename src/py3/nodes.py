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

from data_structure import Node, BufferedLines


class Paragraph(Node):
    inline_types = []

    @classmethod
    def match(cls, text):
        return text and text[0] != ''

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
            cls.log.warning('EOF right after `::`')
            return

        # lstrip blank lines
        blanklines_before = False
        while text and text[0] == '':
            blanklines_before = True
            text.pop(0)
        if not blanklines_before:
            cls.log.warning('Blank line missing before literal block')

        indented = []

        while text and (text[0].startswith(' ') or text[0] == ''):  # XXX: assume space only
            indented.append(text.pop(0))

        if not indented:
            cls.log.warning('None found')
            return

        if text and indented[-1] != '':
            cls.log.warning('Ends without a blank line')

        # remove tailing blank lines
        while indented and indented[-1] == '':
            indented.pop()

        assert indented

        nonempty = filter(None, indented)
        len_leading_space = lambda s: len(s) - len(s.lstrip())
        len_indent = min(map(len_leading_space, nonempty))
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
            """
            :precondition:  1.  `Paragraph` matches non-blank line
                            2.  `LiteralBlock` should match "::" line away

            :additional condition:  should not indent if last line ends with "::"
            """
            last = None
            for lineno, line in enumerate(fetch(cls, text)):
                if lineno == 0:
                    last = line  # let's see whether next line or not
                elif last.endswith('::') and line.startswith(' '):
                    text.insert(0, line)  # insert the indented line back
                    break
                else:
                    yield last  # last is fine
                    last = line

            assert last is not None  # according to 1st precondition

            if last == '::':
                text.insert(0, '::')
            elif m := re.search(r'^(.*?)(\s*)::$', last):  # 'blah::' or 'blah ::'
                text.insert(0, '::')
                yield m.group(1) + ('' if m.group(2) else ':')
            else:
                yield last

        return fetch_

Paragraph.fetch = classmethod(LiteralBlock.patch_paragraph_fetch(Paragraph.fetch.__func__))


class Document(Node):
    # TODO: register them at a package scope settings
    # XXX: require `match`, `fetch`, `parse` methods
    block_types = ['LiteralBlock', 'Paragraph']

    @classmethod
    def parse(cls, text):
        block_types = tuple(map(globals().__getitem__, cls.block_types))

        # TODO: rename to "remove_blank_beginning"
        def lstrip_empty_lines(text):
            while text and text[0] == '':
                text.pop(0)

        # TODO: rename to "parse_block"
        def _parse(text):
            while True:
                lstrip_empty_lines(text)
                if not text:
                    break

                # TODO: rename to "block_type"
                node_type = next(node_type for node_type in block_types if node_type.match(text))
                fetched = BufferedLines(node_type.fetch(text))
                if fetched:
                    yield node_type.parse(fetched)

        return cls(*_parse(text))


class BufferedText(BufferedLines):
    def __init__(self, text):
        lines = map(str.rstrip, text.splitlines())
        super().__init__(lines)
