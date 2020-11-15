function to_lines(text) {
    if (text == '') {
        return [];
    } else if (text.endsWith('\n')) {
        return text.split('\n').slice(0, -1).map(line=>line.trimEnd());
    } else {
        return text.split('\n').map(line=>line.trimEnd());
    }
}


class Node {
    constructor(elems, attrs={}) {
        this.elems = elems;
        this.attr = attrs;
    }
}


class Paragraph extends Node {
    static match = () => true /* (lines.length && lines[0]!='') */;
    static fetch(lines) {
        const fetched = [];
        while (lines.length && lines[0]!='')
            fetched.push(lines.shift());
        return fetched;
    }
    static parse(lines) {
        return new Paragraph(lines);
    }
}


class Document extends Node {
    static block_types = [Paragraph];
    static remove_blank_beginning(lines) {
        while (lines.length && lines[0]=='')
            lines.shift();
    }
    static parse(lines) {
        const elems = [];
        let block_type, fetched;
        while (true) {
            Document.remove_blank_beginning(lines);
            if (!lines.length)
                break;

            block_type = Document.block_types.find(B => B.match(lines));
            fetched = block_type.fetch(lines);
            if (fetched.length)
                elems.push(block_type.parse(fetched));
        }
        return new Document(elems);
    }
}


function parse(text) {
    let lines = to_lines(text);
    return Document.parse(lines);
}


test('split and strip to lines', () => {
    expect(to_lines('')).toEqual([]);
    expect(to_lines(' ')).toEqual(['']);
    expect(to_lines('1')).toEqual(['1']);
    expect(to_lines('\n')).toEqual(['']);
    expect(to_lines('1\n')).toEqual(['1']);
    expect(to_lines('1 \n')).toEqual(['1']);
    expect(to_lines('1\n\n')).toEqual(['1', '']);
});

test('empty document', () => {
    expect(parse('')).toEqual(new Document([]));
    expect(parse('\n')).toEqual(new Document([]));
    expect(parse('\n'.repeat(3))).toEqual(new Document([]));
});

test('paragraph startswith', () => {
    expect(parse('line')).toEqual(
        new Document([
            new Paragraph(['line']),
        ])
    );
    expect(parse('\nline')).toEqual(
        new Document([
            new Paragraph(['line']),
        ])
    );
    expect(parse('\n'.repeat(3) + '\nline')).toEqual(
        new Document([
            new Paragraph(['line']),
        ])
    );
});

test('paragraph endswith', () => {
    expect(parse('line')).toEqual(
        new Document([
            new Paragraph(['line']),
        ])
    );
    expect(parse('line\n' + '\n'.repeat(3))).toEqual(
        new Document([
            new Paragraph(['line']),
        ])
    );
});

test('multi paragraph', () => {
    expect(parse('word 1 word 2\nline 2\n\n\nline 3\n')).toEqual(
        new Document([
            new Paragraph(['word 1 word 2', 'line 2']),
            new Paragraph(['line 3']),
        ])
    );
});
