const Node = (...args) => {
    switch (args.length) {
        case 1: return {name: args[0], attrs: new Map(), elems: []};
        case 2: return {name: args[0], attrs: new Map(), elems: args[1]};
        case 3: return {name: args[0], attrs: args[1], elems: args[2]};
    }
};

const assert = (cond, obj) => {if (!cond) {throw new Error(JSON.stringify(obj))}};

const Parser = {
    parse(text) {
        const lines = text.split(/\r\n|\r|\n/).map(line => line.trimEnd().replace(/\t/g, ' '.repeat(4)));
        return Parser.document(lines, [
            Parser.blank,
            Parser.literal_block,
            Parser.paragraph_chain_literal,
        ]);
    },

    document(lines, block_parsers) {
        const document_node = Node('document');
        let _number_lines, parse, result, offset, elems;

        while (lines.length) {
            _number_lines = lines.length;

            //console.dir({'--->': lines});
            for (let parse of block_parsers) {
                if ((result = parse(lines)) !== undefined) {
                    [offset, elems] = result;
                    lines.splice(0, offset);
                    document_node.elems.push(...elems);
                    //console.dir({_number_lines, lines, offset, parse});
                    break;
                }
            }

            assert((_number_lines > lines.length), [_number_lines, lines]);
        }
        return document_node;
    },

    blank(lines) {
        assert(lines.length, 'the input should be nonempty');

        let offset = 0;
        while (offset < lines.length && lines[offset] == '')
            offset += 1;

        if (offset > 0)
            return [offset, []];
    },

    paragraph_chain_literal(lines) {
        assert(lines.length, 'the input should be nonempty');

        let offset = 0, literal_result;
        while (offset < lines.length && lines[offset] != '') {
            offset += 1;
            if (lines[offset-1].endsWith('::')
                && (literal_result = Parser.literal_block(['::'].concat(lines.slice(offset)))) !== undefined)
                break;
        }

        if (offset == 0)
            return;

        if (literal_result === undefined)
            return [offset, [Node('paragraph', lines.slice(0, offset))]];

        const lastline = lines[offset-1];
        const trailing_colon = lastline.endsWith(' ::') ? '' : ':';
        const paragraph_lines = lines.slice(0, offset-1).concat([lastline.slice(0, -2).trimEnd() + trailing_colon]);
        const nodes = [Node('paragraph', paragraph_lines)];
        const [literal_offset, literal_nodes] = literal_result;

        offset = offset - 1 + literal_offset;
        nodes.push(...literal_nodes);

        return [offset, nodes];
    },

    literal_block(lines) {
        assert(lines.length, 'the input should be nonempty');

        if (lines[0] == '::') {
            if (lines.length == 1) {
                return [1, []];
            } else if (lines[1] == '' || lines[1].startsWith(' ')) {
                /* pass */
            } else {
                return;
            }
        } else {
            return;
        }

        let offset = 1;
        while (offset < lines.length && lines[offset] == '')
            offset += 1;

        const indented = lines.slice(offset).filter(line => line == '' || line.startsWith(' '));
        offset += indented.length;

        if (!indented.length)
            return [offset, []];

        const width = Math.min(...indented.filter(s => s != '').map(s => s.length - s.trimStart().length));
        const dedented = indented.map(s => s == '' ? s : s.slice(width));

        let i = dedented.length;
        while (i > 0 && dedented[i-1] == '')
            i -= 1;
        dedented.splice(i);

        return [offset, [Node('literal_block', dedented)]];
    },
};

export {Node, Parser};
