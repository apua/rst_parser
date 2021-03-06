========================================
Framwork design consideration
========================================

*   the idea workflow:

    1.  parse text stateless → document object
    2.  transform document (more than once maybe) that stateful
    3.  render to HTML

*   consider "given full text, output DOM" only,
    no more requirement like "iter (lazy) DOM" or "partial text modification"

*   "parsing inline w/o given block type" is unreasonable

*   "the end of block" condition always provided

*   processing text line by line with state machine and buffer
    makes it hard to maintain due to implicit state changes;
    I would like replace state machine with call stack,
    and wrap text reading with buffer
    where the wrapped text can be debugable

*   each node type inherit `Node` for data structure
    and bind related methods under the namespace

*   leave `Literal` parse method indepedent with `Paragraph`
    to make parsing block stateless and simpler

*   to keep potentially plugable, "double colon" verification done by
    decorating Paragraph `fetch` method


========================================
Double colons without blank line
========================================

Docutils handle corner case weird.

----

case 1 -- error due to "incomplete section title" ::

    ::::
    line 1
    line 2

IMO, this check is unnecessary, even nonsense;
it is neither title nor transition,
we should treat it as simple as paragraph.

----

case 2 -- info "blank line missing ... interpreted as def" ::

    ::
        line 1
        line 2

IMO, the info is helpful but the result is nonsense,
it is obviously literal because the rare symbol usage

----

Here summarize the order (priority) Docutils identify the text:

#.   section title
#.   definition_list
#.   paragraph
#.   literal_block

In the re-implementation, the order would not the same as Docutils.
