from parser import Parser, Nodes, Node

parse = Parser.parse
document = Nodes.document
paragraph = Nodes.paragraph


class TestInfra:
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
