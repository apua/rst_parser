/*
    Does the same thing as `rst_parser.py` does
*/

class Document {
    constructor() {
    }

    parse() {
        return new Document();
    }
}

// TODO: question -- how to design the namespace for parsing different components?
// TODO: consider `callback` on recursive parsing ?


function parse(text) {
    return "parse text for document"
}


test('empty document', () => {
    expect(parse('')).toEqual(new Document());
    expect(parse('\n')).toEqual(new Document());
    expect(parse('\n'*3)).toEqual(new Document());
});
