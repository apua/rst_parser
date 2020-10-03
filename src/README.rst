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
