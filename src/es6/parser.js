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

const Parser = {
  parse(text) {
    const lines = text.split(/\r\n|\r|\n/).map(line => line.trimEnd().replace(/\t/g, ' '));
    return Parser.document(lines, []);
  },

  document(lines, block_parsers) {
    const document_node = Node('document');
    return document_node;
  },
};

export {Node, Parser};
