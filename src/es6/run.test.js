import {Node, Parser} from './parser.js';


const parse = Parser.parse;

const node = name => (...elems) => Node(name, elems);

const document = node('document');
const paragraph = node('paragraph');
const literal_block = node('literal_block');


describe('Data Structure', () => {
  test('defaults', () => {
    const mynode = {name: 'mynode', attrs: new Map(), elems: []};
    expect(Node('mynode')).toEqual(mynode);
    expect(Node('mynode', [])).toEqual(mynode);
    expect(Node('mynode', new Map(), [])).toEqual(mynode);
  });
});


describe('Document', () => {
  test('empty', () => {
    expect(parse('')).toEqual(document());
    expect(parse('\n')).toEqual(document());
  });

  test('blanks', () => {
    expect(parse(' ')).toEqual(document());
    expect(parse(' \n')).toEqual(document());
    expect(parse('\n ')).toEqual(document());
    expect(parse('\n\n')).toEqual(document());
    expect(parse(' \n\n ')).toEqual(document());
  });

  test('paragraph', () => {
    expect(parse('line')).toEqual(document(paragraph('line')));
    expect(parse('line\nline')).toEqual(document(paragraph('line', 'line')));
  });

  test('eof', () => {
    expect(parse('line\n')).toEqual(document(paragraph('line')));
  });

  test('tab to 4 spaces', () => {
    expect(parse('line\tline')).toEqual(document(paragraph('line    line')));
  });

  test('blanks before paragraph', () => {
    expect(parse('  \nline')).toEqual(document(paragraph('line')));
    expect(parse('  \n\nline')).toEqual(document(paragraph('line')));
  });

  test('blanks after paragraph', () => {
    expect(parse('line\n\n')).toEqual(document(paragraph('line')));
    expect(parse('line\n\n  ')).toEqual(document(paragraph('line')));
  });

  test('multiple paragraphs', () => {
    expect(parse('line\n\nline')).toEqual(document(paragraph('line'), paragraph('line')));
    expect(parse('line\n \nline')).toEqual(document(paragraph('line'), paragraph('line')));
  });
});


describe('Literal Block', () => {
  describe('Hang Colons', () => {
    test('not hang', () => {
      expect(parse('::line')).toEqual(document(paragraph('::line')));
      expect(parse(':: line')).toEqual(document(paragraph(':: line')));
    });

    test('eof', () => {
      expect(parse('::')).toEqual(document());
      expect(parse('::\n')).toEqual(document());
    });

    test('no blanks no indented', () => {
      expect(parse('::\nline')).toEqual(document(paragraph('::', 'line')));
    });

    test('all blanks no indented', () => {
      expect(parse('::\n ')).toEqual(document());
      expect(parse('::\n\n')).toEqual(document());
      expect(parse('::\n \n')).toEqual(document());
      expect(parse('::\n \nline')).toEqual(document(paragraph('line')));
    });

    test('no blank before', () => {
      expect(parse('::\n  literal')).toEqual(document(literal_block('literal')));
      expect(parse('::\n  literal\n\nline')).toEqual(document(literal_block('literal'), paragraph('line')));
    });

    test('no blank after', () => {
      expect(parse('::\n\n  literal\nline')).toEqual(document(literal_block('literal'), paragraph('line')));
    });

    test('no blank before and after', () => {
      expect(parse('::\n  literal\nline')).toEqual(document(literal_block('literal'), paragraph('line')));
    });

    test('literal block', () => {
      expect(parse('::\n\n  literal\n\nline')).toEqual(document(literal_block('literal'), paragraph('line')));
    });
  });

  describe('Paragraph Chain Literal', () => {
    test('chain', () => {
      expect(parse('line::\n\n literal')).toEqual(document(paragraph('line:'), literal_block('literal')));
    });
    test('multiple_paragraphs', () => {
      expect(parse('line\nline::\n\n literal')).toEqual(document(paragraph('line', 'line:'), literal_block('literal')));
      expect(parse('line\nline::\n\n literal\n\nline')).toEqual(document(paragraph('line', 'line:'), literal_block('literal'), paragraph('line')));
    });
    test('trailing_colon', () => {
      expect(parse('line::\n\n literal')).toEqual(document(paragraph('line:'), literal_block('literal')));
      expect(parse('line ::\n\n literal')).toEqual(document(paragraph('line'), literal_block('literal')));
      expect(parse('line  ::\n\n literal')).toEqual(document(paragraph('line'), literal_block('literal')));
      expect(parse('line: ::\n\n literal')).toEqual(document(paragraph('line:'), literal_block('literal')));
      expect(parse('line:::\n\n literal')).toEqual(document(paragraph('line::'), literal_block('literal')));
    });
    test('eof', () => {
      expect(parse('line::')).toEqual(document(paragraph('line:')));
      expect(parse('line::\n')).toEqual(document(paragraph('line:')));
    });
    test('all_blanks_no_indented', () => {
      expect(parse('line::\n ')).toEqual(document(paragraph('line:')));
      expect(parse('line::\n\n')).toEqual(document(paragraph('line:')));
      expect(parse('line::\n \n')).toEqual(document(paragraph('line:')));
      expect(parse('line::\n \nline')).toEqual(document(paragraph('line:'), paragraph('line')));
    });
    test('no_blanks_no_indented', () => {
      expect(parse('line::\nline')).toEqual(document(paragraph('line::', 'line')));
    });
    test('all_blanks_no_indented', () => {
      expect(parse('line::\n\nline')).toEqual(document(paragraph('line:'), paragraph('line')));
    });
    test('no_blank_before_and_after', () => {
      expect(parse('line::\n literal\nline')).toEqual(document(paragraph('line:'), literal_block('literal'), paragraph('line')));
    });
  });
});
