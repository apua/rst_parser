const to_lines = (text) => {
    if (text === '') {
        return [];
    } else if (text.endsWith('\n')) {
        return text.split('\n').slice(0, -1).map(line => line.trimEnd());
    } else {
        return text.split('\n').map(line => line.trimEnd());
    }
}


class Node {
    constructor(...rest) {
        if (rest.length > 0 && rest[0] instanceof Map)
            this.attrs = rest.shift();
        else
            this.attrs = new Map();

        if (rest.length > 0) {
            if (rest[0] instanceof Array) {
                this.elems = rest.shift();
                console.assert(rest.length === 0);
            } else {
                this.elems = rest;
                console.assert(rest.every(elem => elem instanceof Node || typeof elem === 'string'));
            }
        } else {
            this.elems = [];
        }
    }
}


class Paragraph extends Node {
    static match() {
        return true /* (lines.length > 0 && lines[0] != '') */;
    }
    static fetch(lines) {
        const fetched = [];
        while (lines.length > 0 && lines[0] != '')
            fetched.push(lines.shift());
        return fetched;
    }
    static parse(fetched) {
        return new Paragraph([...fetched]);
    }
}


class LiteralBlock extends Node {
    static match(lines) {
        if (lines.length > 0 && lines[0] === '::') {
            if (lines[1] === undefined) {
                return true;
            } else {
                return lines[1] === '' || lines[1].startsWith(' ');
            }
        } else {
            return false;
        }
    }
    static fetch(lines) {
        const colons = lines.shift();
        console.assert(colons === '::');

        if (lines.length === 0) {
            console.warn('EOF right after `::`');
            return [];
        }

        let blanklines_before = false;
        while (lines.length > 0 && lines[0] === '') {
            blanklines_before = true;
            lines.shift();
        }
        if (!blanklines_before)
            console.warn('Blank line missing before literal block');

        const indented = [];

        while (lines.length > 0 && (lines[0].startsWith(' ') || lines[0] === ''))
            indented.push(lines.shift());

        if (indented.length === 0) {
            console.warn('None found');
            return [];
        }

        if (lines.length > 0 && indented[indented.length-1] != '')
            console.warn('Ends without a blank line');

        while (indented.length > 0 && indented[indented.length-1] === '')
            indented.pop();

        console.assert(indented.length > 0);

        const
            nonempty = indented.filter(v => v != ''),
            len_leading_space = s => s.length - s.trimStart().length,
            len_indent = Math.min(...nonempty.map(len_leading_space));
        return indented.map(s => (s != '' ? s.slice(len_indent) : ''));
    }
    static parse(fetched) {
        return new LiteralBlock([...fetched]);
    }
    static patch_paragraph_fetch(fetch) {
    }
}


class Document extends Node {
    static block_types = [LiteralBlock, Paragraph];
    static parse(lines) {
        const elems = [];
        let block_type, fetched;
        while (true) {
            //remove_blank_beginning
            while (lines.length > 0 && lines[0] === '')
                lines.shift();

            if (lines.length === 0)
                break;

            block_type = Document.block_types.find(B => B.match(lines));
            fetched = block_type.fetch(lines);
            if (fetched.length > 0)
                elems.push(block_type.parse(fetched));
        }
        return new Document(elems);
    }
}


const parse = text => Document.parse(to_lines(text));


beforeAll(() => {
    globalThis.assert = {
        to_lines(a, b) {
            expect(to_lines(a)).toEqual(b);
        },
        parse(a, b) {
            expect(parse(a)).toEqual(b);
        },
        lastlogmsg(msg) {
            expect(console.warn).toHaveBeenCalledWith(msg);
            console.warn.mockClear();
        },
    }
});
afterAll(() => {
    delete globalThis.assert;
});
beforeEach(() => {
    console.warn=jest.fn();
});
afterEach(() => {
    jest.restoreAllMocks();
});

test('base class `Node`', () => {
    new Document();
    new Document(['1', '2', new Paragraph('3', '4')]);
    new Document(new Map(Object.entries({'a': 1})), '1', '2', new Paragraph('3', '4'));
});

test('split and strip to lines', () => {
    assert.to_lines('', []);
    assert.to_lines(' ', ['']);
    assert.to_lines('1', ['1']);
    assert.to_lines('\n', ['']);
    assert.to_lines('1\n', ['1']);
    assert.to_lines('1 \n', ['1']);
    assert.to_lines('1\n\n', ['1', '']);
});

test('empty document', () => {
    assert.parse('',new Document());
    assert.parse('\n',new Document());
    assert.parse('\n'.repeat(3),new Document());
});

test('paragraph startswith', () => {
    assert.parse('line',new Document(new Paragraph('line')));
    assert.parse('\nline',new Document(new Paragraph('line')));
    assert.parse('\n'.repeat(3) + '\nline',new Document(new Paragraph('line')));
});

test('paragraph endswith', () => {
    assert.parse('line',new Document(new Paragraph('line')));
    assert.parse('line\n' + '\n'.repeat(3),new Document(new Paragraph('line')));
});

test('multi paragraph', () => {
    assert.parse('word 1 word 2\nline 2\n\n\nline 3\n',
        new Document(new Paragraph('word 1 word 2', 'line 2'), new Paragraph('line 3'))
    );
});

test('literal block hang colons', () => {
    assert.parse('::line',new Document(new Paragraph('::line')));
    assert.parse('::    line',new Document(new Paragraph('::    line')));
    assert.parse('::\nline',new Document(new Paragraph('::', 'line')));

    assert.parse('::\n  literal',new Document(new LiteralBlock('literal')));
    assert.lastlogmsg('Blank line missing before literal block');

    assert.parse('::\n\n  literal',new Document(new LiteralBlock('literal')));
    assert.parse('::\n\n  literal\nline',new Document(new LiteralBlock('literal'), new Paragraph('line')));
    assert.lastlogmsg('Ends without a blank line');
    assert.parse('::\n\n  literal\n\nline',new Document(new LiteralBlock('literal'), new Paragraph('line')));

    assert.parse('::', new Document());
    assert.lastlogmsg('EOF right after `::`');
    assert.parse('::\n\n\n', new Document());
    assert.lastlogmsg('None found');
    assert.parse('::\n\n\nline', new Document(new Paragraph('line')));
    assert.lastlogmsg('None found');
});
