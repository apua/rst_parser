from nodes import *


def parse(text):
    text = BufferedText(text)
    return Document.parse(text)


def test_multi_paragraph():
    s = (
            'word 1 word 2\n'
            'line 2\n'
            '\n'
            '\n'
            'line 3\n'
            )
    d = Document(
            Paragraph('word 1 word 2\nline 2'),
            Paragraph('line 3'),
            )
    assert parse(s) == d


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
