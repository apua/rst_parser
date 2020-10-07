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
