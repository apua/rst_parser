from parser import Parser, Node

parse = Parser.parse

def node(name):
    """
    >>> document()
    Node(name='document', attrs={}, elems=[])
    >>> document('a', 'b', 'c')
    Node(name='document', attrs={}, elems=['a', 'b', 'c'])
    """
    return lambda *elems: Node(name, elems=list(elems))

document = node('document')
paragraph = node('paragraph')
literal_block = node('literal_block')


class TestDataStructure:
    def test_data_structure(self):
        assert Node('') == Node('', {}, [])

    def test_calling_parser(self):
        assert document() == Node('document')
        assert paragraph() == Node('paragraph')


class TestDocument:
    def test_empty_document(self):
        assert parse('') == document()
        assert parse(' ') == document()
        assert parse('\n') == document()
        assert parse('\n\n') == document()
        assert parse('\n  \n  ') == document()

    def test_startswith_blanks(self):
        assert parse('line') == document(paragraph('line'))
        assert parse('  \nline') == document(paragraph('line'))
        assert parse('  \n\nline') == document(paragraph('line'))

    def test_endswith_blanks(self):
        assert parse('line') == document(paragraph('line'))
        assert parse('line\n\n') == document(paragraph('line'))
        assert parse('line\n\n  \n') == document(paragraph('line'))

    def test_multiple_nodes(self):
        assert parse('a\nb\n\nc\n') == document(paragraph('a', 'b'), paragraph('c'))


class TestLiteralBlock:
    class TestHangColons:
        def test_trailing_string(self):
            assert parse('::line') == document(paragraph('::line'))
            assert parse('::    line') == document(paragraph('::    line'))

        def test_eof(self):
            # system_message warning "Literal block expected; none found."
            assert parse('::') == document()
            assert parse('::\n') == document()
            assert parse('::\n\n') == document()

        def test_neither_blank_nor_indent(self):
            # system_message info "Treating the overline as ordinary text because it's so short."
            assert parse('::\nline') == document(paragraph('::', 'line'))

        def test_no_indent(self):
            # system_message warning "Literal block expected; none found."
            assert parse('::\n\n') == document()
            assert parse('::\n\nline') == document(paragraph('line'))

        def test_no_blank_before(self):
            # system_message error "Unexpected indentation."
            assert parse('::\n  literal') == document(literal_block('literal'))
            assert parse('::\n  literal\n\nline') == document(literal_block('literal'), paragraph('line'))

        def test_no_blank_after(self):
            # system_message warning "Literal block ends without a blank line; unexpected unindent."
            assert parse('::\n\n  literal\nline') == document(literal_block('literal'), paragraph('line'))

        def test_no_blank_before_and_after(self):
            # system_message error "Unexpected indentation."
            # system_message warning "Literal block ends without a blank line; unexpected unindent."
            assert parse('::\n  literal\nline') == document(literal_block('literal'), paragraph('line'))

        def test_normal_literal(self):
            assert parse('::\n\n  literal\n\nline') == document(
                    literal_block('literal'), paragraph('line'))

    class TestParagraphChainLiteral:
        def test_chain(self):
            assert parse('line::\n\n literal') == document(
                    paragraph('line:'), literal_block('literal'))
            assert parse('line\nline::\n\n literal') == document(
                    paragraph('line', 'line:'), literal_block('literal'))
            assert parse('line\nline::\n\n literal\n\nline') == document(
                    paragraph('line', 'line:'), literal_block('literal'), paragraph('line'))

        def test_trailing_colon(self):
            assert parse('line::\n\n literal') == document(paragraph('line:'), literal_block('literal'))
            assert parse('line ::\n\n literal') == document(paragraph('line'), literal_block('literal'))
            assert parse('line  ::\n\n literal') == document(paragraph('line'), literal_block('literal'))
            assert parse('line: ::\n\n literal') == document(paragraph('line:'), literal_block('literal'))
            assert parse('line:::\n\n literal') == document(paragraph('line::'), literal_block('literal'))

        def test_eof(self):
            # system_message warning "Literal block expected; none found."
            assert parse('line::') == document(paragraph('line:'))
            assert parse('line::\n') == document(paragraph('line:'))
            assert parse('line::\n\n') == document(paragraph('line:'))

        def test_none_indented_after_double_colons(self):
            assert parse('line::\nline') == document(paragraph('line::', 'line'))

        def test_blank_after_double_colons(self):
            # system_message warning "Literal block expected; none found."
            assert parse('line::\n\nline') == document(paragraph('line:'), paragraph('line'))

        def test_literal_no_blank_before_and_after(self):
            # system_message error "Unexpected indentation."
            # system_message warning "Literal block ends without a blank line; unexpected unindent.'
            assert parse('line::\n literal\nline') == document(
                    paragraph('line:'), literal_block('literal'), paragraph('line'))
