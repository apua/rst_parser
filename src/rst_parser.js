/*
    Does the same thing as `rst_parser.py` does
*/

const Document = Symbol();
const Paragraph = Symbol();


function parse(text) {
    return text;
}

sample_123 = (
    'blah blah blah blah\n'+ 
    'blah blah blah blah   \n'+
    '\n'+
    'blah blah blah blah\t\n'+
    '')

dom_123 = {'tag': Document, 'elements': [
    {'tag': Paragraph, 'elements': ['blah blah blah blah', 'blah blah blah blah']},
    {'tag': Paragraph, 'elements': ['blah blah blah blah']},
    ]}

test('sample', () => {
  expect(parse(sample_123)).toEqual(sample_123);
});
