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
    def __init__(self, *nodes, **attrs):
        self.nodes = nodes
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
        for node in self.nodes:
            if isinstance(node, Node):
                yield from (f'{indent}{line}' for line in node.reprlines())
            else:
                yield f'{indent}{node!r}'

    def __repr__(self):
        return '\n'.join(self.reprlines())

    def __eq__(self, n):
        return self.__class__ == n.__class__ \
                and self.attrs == n.attrs \
                and self.nodes == n.nodes
