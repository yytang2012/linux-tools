#!/usr/bin/env python
# coding=utf-8

"""
A Python implementation of the FP-growth algorithm.
Basic usage of the module is very simple:
    > from fp_growth import find_frequent_itemsets
    > find_frequent_itemsets(transactions, minimum_support)
"""
import os
from collections import defaultdict, namedtuple
from queue import Queue

from misc import get_percentage

__author__ = 'Yutao Tang <yytang@email.wm.edu>'
__copyright__ = 'Copyright © 2016 '
__license__ = 'MIT License'


class FPTree(object):
    """
    An FP tree.
    This object may only store transaction items that are hashable
    (i.e., all items must be valid as dictionary keys or set members).
    """

    Route = namedtuple('Route', 'head tail')

    def __init__(self):
        self._next_identity = 0
        # The root node of the tree.
        self._root = FPNode(self, None, None, identity=self.get_next_identity())

        # A dictionary mapping items to the head and tail of a path of
        # "neighbors" that will hit every node containing that item.
        self._routes = {}

    def get_next_identity(self):
        identity = self._next_identity
        self._next_identity += 1
        return identity;

    @property
    def root(self):
        """The root node of the tree."""
        return self._root

    def add(self, transaction):
        """Add a transaction to the tree."""
        point = self._root

        for item in transaction:
            next_point = point.search(item)
            if next_point:
                # There is already a node in this tree for the current
                # transaction item; reuse it.
                next_point.increment()
            else:
                # Create a new point and add it as a child of the point we're
                # currently looking at.
                next_point = FPNode(self, item, identity=self.get_next_identity())
                point.add(next_point)

                # Update the route of nodes that contain this item to include
                # our new node.
                self._update_route(next_point)

            point = next_point

    def _update_route(self, point):
        """Add the given node to the route through all nodes for its item."""
        assert self is point.tree

        try:
            route = self._routes[point.item]
            route[1].neighbor = point  # route[1] is the tail
            self._routes[point.item] = self.Route(route[0], point)
        except KeyError:
            # First node for this item; start a new route.
            self._routes[point.item] = self.Route(point, point)

    def items(self):
        """
        Generate one 2-tuples for each item represented in the tree. The first
        element of the tuple is the item itself, and the second element is a
        generator that will yield the nodes in the tree that belong to the item.
        """
        for item in self._routes.keys():
            yield (item, self.nodes(item))

    def nodes(self, item):
        """
        Generate the sequence of nodes that contain the given item.
        """

        try:
            node = self._routes[item][0]
        except KeyError:
            return

        while node:
            yield node
            node = node.neighbor

    def prefix_paths(self, item):
        """Generate the prefix paths that end with the given item."""

        def collect_path(node):
            path = []
            while node and not node.root:
                path.append(node)
                node = node.parent
            path.reverse()
            return path

        return (collect_path(node) for node in self.nodes(item))


class FPNode(object):
    """A node in an FP tree."""

    def __init__(self, tree, item, count=1, identity=0):
        self._tree = tree
        self._item = item
        self._count = count
        self._identity = identity
        self._parent = None
        self._children = {}
        self._neighbor = None

    def add(self, child):
        """Add the given FPNode `child` as a child of this node."""

        if not isinstance(child, FPNode):
            raise TypeError("Can only add other FPNodes as children")

        if not child.item in self._children:
            self._children[child.item] = child
            child.parent = self

    def search(self, item):
        """
        Check whether this node contains a child node for the given item.
        If so, that node is returned; otherwise, `None` is returned.
        """
        try:
            return self._children[item]
        except KeyError:
            return None

    def __contains__(self, item):
        return item in self._children

    @property
    def tree(self):
        """The tree in which this node appears."""
        return self._tree

    @property
    def item(self):
        """The item contained in this node."""
        return self._item

    @property
    def count(self):
        """The count associated with this node's item."""
        return self._count

    def increment(self):
        """Increment the count associated with this node's item."""
        if self._count is None:
            raise ValueError("Root nodes have no associated count.")
        self._count += 1

    @property
    def identity(self):
        """The identity associated with this node"""
        return self._identity

    @property
    def root(self):
        """True if this node is the root of a tree; false if otherwise."""
        return self._item is None and self._count is None

    @property
    def leaf(self):
        """True if this node is a leaf in the tree; false if otherwise."""
        return len(self._children) == 0

    @property
    def parent(self):
        """The node's parent"""
        return self._parent

    @parent.setter
    def parent(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a parent.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a parent from another tree.")
        self._parent = value

    @property
    def neighbor(self):
        """
        The node's neighbor; the one with the same value that is "to the right"
        of it in the tree.
        """
        return self._neighbor

    @neighbor.setter
    def neighbor(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as a neighbor.")
        if value and value.tree is not self.tree:
            raise ValueError("Cannot have a neighbor from another tree.")
        self._neighbor = value

    @property
    def children(self):
        """The nodes that are children of this node."""
        return tuple(self._children.values())

    def inspect(self, depth=0):
        print('  ' * depth) + repr(self)
        for child in self.children:
            child.inspect(depth + 1)

    def __repr__(self):
        if self.root:
            return "<%s (root)>" % type(self).__name__
        return "<%s %r (%r)>" % (type(self).__name__, self.item, self.count)


def find_frequent_itemsets(transactions, minimum_support_percent, include_support=False, output_name="graph"):
    """
    Find frequent itemsets in the given transactions using FP-growth. This
    function returns a generator instead of an eagerly-populated list of items.
    The `transactions` parameter can be any iterable of iterables of items.
    `minimum_support` should be an integer specifying the minimum number of
    occurrences of an itemset for it to be accepted.
    Each item must be hashable (i.e., it must be valid as a member of a
    dictionary or a set).
    If `include_support` is true, yield (itemset, support) pairs instead of
    just the itemsets.
    """
    total_set_num = len(transactions)
    minimum_support = int(total_set_num * minimum_support_percent / 100)
    print("minimum support value is : %d" % minimum_support)
    items_raw = defaultdict(lambda: 0)  # mapping from items to their supports

    # Load the passed-in transactions and count the support that individual
    # items have.
    for transaction in transactions:
        for item in transaction:
            items_raw[item] += 1

    items = {};
    # Remove infrequent items from the item support dictionary.

    for item, support in items_raw.items():
        if support >= minimum_support:
            items[item] = support;
    print(items)

    # Build our FP-tree. Before any transactions can be added to the tree, they
    # must be stripped of infrequent items and their surviving items must be
    # sorted in decreasing order of frequency.

    def clean_transaction(transaction):
        new_transaction = list(filter(lambda v: v in items, transaction));
        new_transaction.sort(key=lambda v: (-items[v], v))
        # new_transaction.sort()
        return new_transaction

    master = FPTree()
    for transaction in map(clean_transaction, transactions):
        master.add(transaction)

    def print_graph(master, minsup, name='graph'):
        if name[-len('.dot'):] != '.dot':
            graph_name = name + '.dot'
        else:
            graph_name = name
        folder_path = '/home/ami/yutang/Data-Reduction-Output/The-25th-Week'
        folder_path = os.path.expanduser(folder_path)
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)
        graph_path = os.path.join(folder_path, graph_name)
        root = master.root;
        graph_descs = []
        build_graph(None, root, minsup, graph_descs=graph_descs);
        with open(graph_path, 'w') as f:
            f.write('digraph{\n')
            for desc in graph_descs:
                f.write("    %s\n" % desc)
            f.write('}\n')

    def build_graph(parent, root, minsup, graph_descs):
        q = Queue()
        q.put(root)
        while not q.empty():
            tmp_node = q.get()
            if tmp_node.item is None:
                desc = '%d [label="Root"];' % tmp_node.identity
                graph_descs.append(desc)
            else:
                desc = '%d [label="%s"];' % (tmp_node.identity, tmp_node.item)
                graph_descs.append(desc)
            tmp_neighbor = tmp_node.neighbor
            while tmp_neighbor is not None and tmp_neighbor.count < minsup:
                tmp_neighbor = tmp_neighbor.neighbor

            if tmp_neighbor is not None:
                print(
                    "neighbor: %s-%d --> %s-%d" % (
                    tmp_node.item, tmp_node.identity, tmp_neighbor.item, tmp_neighbor.identity))
                desc = '%d -> %d [style=dotted];' % (tmp_node.identity, tmp_neighbor.identity)
                graph_descs.append(desc)
            for child in tmp_node.children:
                if child.count < minsup:
                    continue
                print("%s-%d -> %s-%d : %d" % (
                    tmp_node.item, tmp_node.identity, child.item, child.identity, child.count))
                desc = '%d -> %d [color=blue, label="%d(%s)"];' % \
                       (tmp_node.identity, child.identity, child.count, get_percentage(child.count, total_set_num))
                graph_descs.append(desc)
                q.put(child)

    print_graph(master, minimum_support, name=output_name);

    def find_with_suffix(tree, suffix):
        for item, nodes in tree.items():
            support = sum(n.count for n in nodes)
            if support >= minimum_support and item not in suffix:
                # New winner!
                found_set = [item] + suffix
                yield (found_set, support) if include_support else found_set

                # Build a conditional tree and recursively search for frequent
                # itemsets within it.
                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item))
                for s in find_with_suffix(cond_tree, found_set):
                    yield s  # pass along the good news to our caller

                    # Search for frequent itemsets, and yield the results we find.
                    # for itemset in find_with_suffix(master, []):
                    #     yield itemset


def conditional_tree_from_paths(paths):
    """Build a conditional FP-tree from the given prefix paths."""
    tree = FPTree()
    condition_item = None
    items = set()

    # Import the nodes in the paths into the new tree. Only the counts of the
    # leaf notes matter; the remaining counts will be reconstructed from the
    # leaf counts.
    for path in paths:
        if condition_item is None:
            condition_item = path[-1].item

        point = tree.root
        for node in path:
            next_point = point.search(node.item)
            if not next_point:
                # Add a new node to the tree.
                items.add(node.item)
                count = node.count if node.item == condition_item else 0
                next_point = FPNode(tree, node.item, count)
                point.add(next_point)
                tree._update_route(next_point)
            point = next_point

    assert condition_item is not None

    # Calculate the counts of the non-leaf nodes.
    for path in tree.prefix_paths(condition_item):
        count = path[-1].count
        for node in reversed(path[:-1]):
            node._count += count

    return tree


def print_fp_tree(transactions, min_percent=1, output_name='graph'):
    new_transactions = []
    file_name_to_value_map = {};
    count = 0
    for transaction in transactions:
        new_transaction = [];
        for item in transaction:
            if item not in file_name_to_value_map:
                count += 1
                file_name_to_value_map[item] = count
                new_transaction.append(file_name_to_value_map[item])
            else:
                new_transaction.append(file_name_to_value_map[item])
        new_transactions.append(new_transaction)

    find_frequent_itemsets(new_transactions, min_percent, True, output_name="%s-%d-percent" % (output_name, min_percent))


if __name__ == '__main__':
    transactions = [['a', 'b'], ['b', 'c', 'd'], ['a', 'c', 'd', 'e'], ['a', 'd', 'e'], ['a', 'b', 'c'],
                    ['a', 'b', 'c', 'd'], ['a'], ['a', 'b', 'c'], ['a', 'b', 'd'], ['b', 'c', 'e'], ['b', 'c', 'd'],
                    ['b', 'c', 'd'], ['b', 'c', 'd'], ['b', 'c', 'd']]
    minsup = 1;

    result = []
    count = 22
    print_fp_tree(transactions, minsup, output_name='f%d' % count)
