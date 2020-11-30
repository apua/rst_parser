from nodes import *


def parse(text):
    # TODO: rename corresponding from "text" to "lines"
    text = BufferedText(text)
    return Document.parse(text)


def test_empty_document():
    assert parse('') == Document()
    assert parse('\n') == Document()
    assert parse('\n'*3) == Document()

def test_paragraph_startswith():
    assert parse('line') == Document(Paragraph('line'))
    assert parse('\nline') == Document(Paragraph('line'))
    assert parse('\n'*3 + '\nline') == Document(Paragraph('line'))

def test_paragraph_endswith():
    assert parse('line') == Document(Paragraph('line'))
    assert parse('line\n' + '\n'*3) == Document(Paragraph('line'))

def test_multi_paragraph():
    assert parse('word 1 word 2\nline 2\n\n\nline 3\n') == \
            Document(Paragraph('word 1 word 2', 'line 2'), Paragraph('line 3'))

def test_literal_block_hang_colons(caplog):
    lastlogmsg = lambda: (r := caplog.records[-1]) and caplog.clear() or r.message

    assert parse('::line') == Document(Paragraph('::line'))
    assert parse('::    line') == Document(Paragraph('::    line'))
    assert parse('::\nline') == Document(Paragraph('::', 'line'))

    # in Docutils, it is definition with info literal;
    # in this implementation, it is a literal block
    assert parse('::\n  literal') == Document(LiteralBlock('literal'))
    assert lastlogmsg() == 'Blank line missing before literal block'

    assert parse('::\n\n  literal') == Document(LiteralBlock('literal'))
    assert parse('::\n\n  literal\nline') == Document(LiteralBlock('literal'), Paragraph('line'))
    assert lastlogmsg() == 'Ends without a blank line'
    assert parse('::\n\n  literal\n\nline') == Document(LiteralBlock('literal'), Paragraph('line'))

    # in Docutils, below warns literal block expected
    assert parse('::') == Document()
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('::\n\n\n') == Document()
    assert lastlogmsg() == 'None found'
    assert parse('::\n\n\nline') == Document(Paragraph('line'))
    assert lastlogmsg() == 'None found'

def test_literal_block_eof(caplog):
    lastlogmsg = lambda: (r := caplog.records[-1]) and caplog.clear() or r.message

    # in Docutils, below warns literal block expected

    assert parse('line ::') == Document(Paragraph('line'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line   ::') == Document(Paragraph('line'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line\n::') == Document(Paragraph('line'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line\n\n\n::') == Document(Paragraph('line'))
    assert lastlogmsg() == 'EOF right after `::`'

    assert parse('line::') == Document(Paragraph('line:'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line::\n') == Document(Paragraph('line:'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line::\n\n\n') == Document(Paragraph('line:'))
    assert lastlogmsg() == 'None found'

    assert parse('line: ::') == Document(Paragraph('line:'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line: ::\n') == Document(Paragraph('line:'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line: ::\n\n\n') == Document(Paragraph('line:'))
    assert lastlogmsg() == 'None found'

    assert parse('line:::') == Document(Paragraph('line::'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line:::\n') == Document(Paragraph('line::'))
    assert lastlogmsg() == 'EOF right after `::`'
    assert parse('line:::\n\n\n') == Document(Paragraph('line::'))
    assert lastlogmsg() == 'None found'

def test_literal_block(caplog):
    lastlogmsg = lambda: (r := caplog.records[-1]) and caplog.clear() or r.message

    assert parse('line::\nline') == Document(Paragraph('line::', 'line'))

    # in Docutils, it warns literal block expected
    assert parse('line::\n\nline') == Document(Paragraph('line:'), Paragraph('line'))
    assert lastlogmsg() == 'None found'

    # in Document, it is definition
    assert parse('line::\n literal') == Document(Paragraph('line:'), LiteralBlock('literal'))
    assert lastlogmsg() == 'Blank line missing before literal block'

    assert parse('line::\n\n literal') == Document(Paragraph('line:'), LiteralBlock('literal'))
    assert parse('line::\n\n\n literal') == Document(Paragraph('line:'), LiteralBlock('literal'))

    assert parse('line::\n\n literal\n literal\n\nline') == \
            Document(Paragraph('line:'), LiteralBlock('literal', 'literal'), Paragraph('line'))
