const Node = (...args) => {
  switch (args.length) {
    case 1:
      return {name: args[0], attrs: new Map(), elems: []};
    case 2:
      return {name: args[0], attrs: new Map(), elems: args[1]};
    case 3:
      return {name: args[0], attrs: args[1], elems: args[2]};
  }
};


const repr = JSON.stringify;


const Parser = {
  parse(text) {
    const lines = text.split(/\r\n|\r|\n/).map(line => line.trimEnd().replace(/\t/g, ' '));
    return Parser.document(lines, [
      Parser.blank,
      //Parser.paragraph,
    ]);
  },

  document(lines, block_parsers) {
    const document_node = Node('document');
    let _number_lines, parse, result, offset, elems;

    while (lines.length) {
      _number_lines = lines.length;

      for (let parse of block_parsers) {
        if ((result = parse(lines)) !== undefined) {
          [offset, elems] = result;
          lines.splice(0, offset);
          //document_node.elems += elems
          break;
        }
      }

      console.assert((_number_lines > lines.length), `${repr(_number_lines)}, ${repr(lines)}`);
      (_number_lines > lines.length) ||  null.assertion_error;
    }
    return document_node;
  },

  blank(lines) {
    console.assert(lines.length, 'nonempty_input');

    let offset, line;

    offset = 0;
    for (line of lines) {
        if (line == '') {
            offset += 1;
        } else {
            break;
        }
    }

    if (offset > 0)
      return [offset, []];
  },

  paragraph(lines) {
    console.assert(lines.length, 'nonempty_input');

    let offset;
  },
};

export {Node, Parser};
