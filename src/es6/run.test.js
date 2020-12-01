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
});
