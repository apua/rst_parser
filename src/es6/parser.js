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

const assert = (cond, obj) => {if (!cond) {throw new Error(JSON.stringify(obj))}};

const Parser = {
  parse(text) {
    const lines = text.split(/\r\n|\r|\n/).map(line => line.trimEnd().replace(/\t/g, ' '.repeat(4)));
    return Parser.document(lines, [
      Parser.blank,
      Parser.paragraph,
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
    assert(lines.length, 'the input should be nonempty');

    let offset, line;

    offset = 0;
    for (line of lines) {
      if (line != '') {
        offset += 1;
      } else {
          break;
      }
    }

    if (offset > 0)
      return [offset, [Node('paragraph', lines.slice(0, offset))]];
  },
};

export {Node, Parser};
