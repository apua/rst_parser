import logging
from typing import List


logging.basicConfig(format='{levelname}:{name}:{message}', level=logging.DEBUG, style='{')


class ClassLogger(type):
    def __new__(mcls, name, bases, namespace, **kw):
        cls = super().__new__(mcls, name, bases, namespace, **kw)
        cls.log = logging.getLogger(name)
        return cls


class Node(metaclass=ClassLogger):
    r"""
    >>> Node()
    <Node>
    >>> Node(['1', '2'])
    <Node>
        '1'
        '2'
    >>> Node('1', '2')  # for convenience
    <Node>
        '1'
        '2'
    >>> Node({'a': 1}, Node('1'), Node({'b': 2}, ['3']))
    <Node {'a': 1}>
        <Node>
            '1'
        <Node {'b': 2}>
            '3'
    """
    def __init__(self, *args):
        rest = list(args)
        if rest and isinstance(rest[0], dict):
            self.attrs = rest.pop(0)
        else:
            self.attrs = {}

        if rest:
            if isinstance(rest[0], list):
                self.elems = rest.pop(0)
                assert len(rest) == 0
            else:
                self.elems = rest
                assert all(isinstance(elem, (Node, str)) for elem in self.elems)
        else:
            self.elems = []

    def __eq__(self, node):
        return all(getattr(self, key) == getattr(node, key) for key in ('__class__', 'attrs', 'elems'))

    def reprlines(self):
        if self.attrs:
            tag = f'<{self.__class__.__name__} {self.attrs}>'
        else:
            tag = f'<{self.__class__.__name__}>'
        yield tag

        indent = ' ' * 4
        for node in self.elems:
            if isinstance(node, Node):
                yield from (f'{indent}{line}' for line in node.reprlines())
            else:
                yield f'{indent}{node!r}'

    def __repr__(self):
        return '\n'.join(self.reprlines())

    def __str__(self):
        return repr(self)


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
