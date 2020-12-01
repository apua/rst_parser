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
});
