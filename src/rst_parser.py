r"""
reStructuredText Parser

1.  Parse stateless line-based components
2.  During parsing line-based components,
    parse stateless inline components
3.  Calculate DOM to stateful
4.  Render from DOM
"""

# XXX: consider "given full text, output DOM" only,
#      no more requirement like "iter (lazy) DOM" or "partial text modification"

# XXX: "parsing inline w/o given block type" is unreasonable

# XXX: "the end of block" condition always provided

# XXX: processing text line by line with state machine and buffer
#      makes it hard to maintain due to implicit state changes;
#      I would like replace state machine with call stack,
#      and wrap text reading with buffer
#      where the wrapped text can be debugable

# XXX: each node type inherit `Node` for data structure
#      and bind related methods under the namespace

# XXX: leave `Literal` parse method indepedent with `Paragraph`
#      to make parsing block stateless and simpler

# XXX: to keep potentially plugable, "double colon" verification done by
#      decorating Paragraph `fetch` method

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
