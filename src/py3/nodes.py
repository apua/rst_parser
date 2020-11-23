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
    def match(cls, lines):
        return lines and lines[0] != ''

    @classmethod
    def fetch(cls, lines):
        while lines and lines[0] != '':
            yield lines.pop(0)

    @classmethod
    def parse(cls, lines):
        return cls(*lines)


class LiteralBlock(Node):
    @classmethod
    def match(cls, lines):
        if lines and lines[0] == '::':
            try:
                line = lines[1]
            except IndexError:
                return True
            else:
                return line == '' or line.startswith(' ')
        else:
            return False

    @classmethod
    def fetch(cls, lines):
        # remove colons
        colons = lines.pop(0)
        assert colons == '::'

        if not lines:
            cls.log.warning('EOF right after `::`')
            return

        # remove leading blank lines
        blanklines_before = False
        while lines and lines[0] == '':
            blanklines_before = True
            lines.pop(0)
        if not blanklines_before:
            cls.log.warning('Blank line missing before literal block')

        indented = []

        while lines and (lines[0].startswith(' ') or lines[0] == ''):  # XXX: assume space only
            indented.append(lines.pop(0))

        if not indented:
            cls.log.warning('None found')
            return

        if lines and indented[-1] != '':
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
    def parse(cls, lines):
        return cls(*lines)

    @staticmethod
    def patch_paragraph_fetch(fetch):
        import functools
        import re

        @functools.wraps(fetch)
        def fetch_(cls, lines):
            """
            :precondition:  1.  `Paragraph` matches non-blank line
                            2.  `LiteralBlock` should match "::" line away

            :additional condition:  should not indent if last line ends with "::"
            """
            last = None
            for lineno, line in enumerate(fetch(cls, lines)):
                if lineno == 0:
                    last = line  # let's see whether next line or not
                elif last.endswith('::') and line.startswith(' '):
                    lines.insert(0, line)  # insert the indented line back
                    break
                else:
                    yield last  # last is fine
                    last = line

            assert last is not None  # according to 1st precondition

            if last == '::':
                lines.insert(0, '::')
            elif m := re.search(r'^(.*?)(\s*)::$', last):  # 'blah::' or 'blah ::'
                lines.insert(0, '::')
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
    def parse(cls, lines):
        block_types = tuple(map(globals().__getitem__, cls.block_types))

        def remove_leading_blanks(lines):
            while lines and lines[0] == '':
                lines.pop(0)

        def parse_block(lines):
            while True:
                remove_leading_blanks(lines)
                if not lines:
                    break

                block_type = next(bt for bt in block_types if bt.match(lines))
                fetched = BufferedLines(block_type.fetch(lines))
                if fetched:
                    yield block_type.parse(fetched)

        return cls(*parse_block(lines))


class BufferedText(BufferedLines):
    def __init__(self, text):
        lines = map(str.rstrip, text.splitlines())
        super().__init__(lines)
