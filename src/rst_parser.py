from nodes import *


def parse(text):
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

def test_literal_block_hang_colons():
    assert parse('::line') == Document(Paragraph('::line'))
    assert parse('::    line') == Document(Paragraph('::    line'))
    assert parse('::\nline') == Document(Paragraph('::', 'line'))

    # in Docutils, it is definition with info literal;
    # in this implementation, it is a literal block
    # [WARN][LiteralBlock] Blank line missing before literal block
    assert parse('::\n  literal') == Document(LiteralBlock('literal'))

    assert parse('::\n\n  literal') == Document(LiteralBlock('literal'))
    # [WARN][LiteralBlock] Ends without a blank line
    assert parse('::\n\n  literal\nline') == Document(LiteralBlock('literal'), Paragraph('line'))
    assert parse('::\n\n  literal\n\nline') == Document(LiteralBlock('literal'), Paragraph('line'))

    # in Docutils, below warns literal block expected
    # [WARN][LiteralBlock] EOF right after `::`
    assert parse('::') == Document(LiteralBlock())
    # [WARN][LiteralBlock] None found
    assert parse('::\n\n\n') == Document(LiteralBlock())
    # [WARN][LiteralBlock] None found
    assert parse('::\n\n\nline') == Document(LiteralBlock(), Paragraph('line'))

def test_literal_block_eof():
    # in Docutils, below warns literal block expected
    assert parse('line::') == Document(Paragraph('line:'), LiteralBlock())
    assert parse('line::\n') == Document(Paragraph('line:'), LiteralBlock())
    assert parse('line::\n\n\n') == Document(Paragraph('line:'), LiteralBlock())
    assert parse('line ::') == Document(Paragraph('line'), LiteralBlock())
    assert parse('line   ::') == Document(Paragraph('line'), LiteralBlock())
    assert parse('line\n::') == Document(Paragraph('line'), LiteralBlock())
    assert parse('line\n\n\n::') == Document(Paragraph('line'), LiteralBlock())

def test_literal_block():
    assert parse('line::\nline') == Document(Paragraph('line::', 'line'))

    # in Docutils, it warns literal block expected
    assert parse('line::\n\nline') == Document(Paragraph('line:'), LiteralBlock(), Paragraph('line'))

    # in Document, it is definition
    assert parse('line::\n literal') == Document(Paragraph('line:'), LiteralBlock('literal'))

    assert parse('line::\n\n literal') == Document(Paragraph('line:'), LiteralBlock('literal'))
    assert parse('line::\n\n\n literal') == Document(Paragraph('line:'), LiteralBlock('literal'))

    assert parse('line::\n\n literal\n literal\n\nline') == \
            Document(Paragraph('line:'), LiteralBlock('literal', 'literal'), Paragraph(line))
