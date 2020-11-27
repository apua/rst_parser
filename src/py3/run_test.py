from parser import *


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
