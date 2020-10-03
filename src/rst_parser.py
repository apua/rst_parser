from nodes import *


def parse(text):
    text = BufferedText(text)
    return Document.parse(text)


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
