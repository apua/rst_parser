from typing import List


class Node:
    r"""
    >>> Node(Node(1), Node('2', [3]), a=1)
    <Node {'a': 1}>
        <Node>
            1
        <Node>
            '2'
            [3]
    """
    def __init__(self, *elems, **attrs):
        self.elems = elems
        self.attrs = attrs

    def __str__(self):
        return repr(self)

    @property
    def tag(self) -> str:
        if self.attrs:
            return f'<{self.__class__.__name__} {self.attrs}>'
        else:
            return f'<{self.__class__.__name__}>'

    def reprlines(self) -> List[str]:
        indent = ' ' * 4
        yield self.tag
        for node in self.elems:
            if isinstance(node, Node):
                yield from (f'{indent}{line}' for line in node.reprlines())
            else:
                yield f'{indent}{node!r}'

    def __repr__(self):
        return '\n'.join(self.reprlines())

    def __eq__(self, n):
        return self.__class__ == n.__class__ \
                and self.attrs == n.attrs \
                and self.elems == n.elems


class BufferedLines:
    def __init__(self, lines):
        import collections
        assert isinstance(lines, collections.abc.Iterator)
        self._lines = lines
        self._buffer = []
        self._is_empty = False

    def _readline(self):
        return self._buffer.append(next(self._lines))

    def __bool__(self):
        if self._buffer:
            return True

        if self._is_empty:
            return False

        try:
            self._readline()
        except StopIteration:
            self._is_empty = True
            return False
        else:
            return True

    def __getitem__(self, idx):
        if not (isinstance(idx, int) and idx >= 0):
            raise TypeError

        if self._is_empty:
            raise IndexError

        lack = idx + 1 - len(self._buffer)

        if lack <= 0:
            return self._buffer[idx]

        try:
            for i in range(lack):
                self._readline()
        except StopIteration:
            raise IndexError
        else:
            return self._buffer[idx]

    def __iter__(self):
        yield from self._buffer
        yield from self._lines

    def clear(self):
        self._buffer.clear()
        self._is_empty = True

    def pop(self, idx):
        self[idx]  # ensure the value exists
        return self._buffer.pop(idx)

    def insert(self, idx, v):
        self._buffer.insert(idx, v)
        self._is_empty = False
