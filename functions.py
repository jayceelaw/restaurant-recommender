""" TODO: docstring """

from __future__ import annotations

import csv
from typing import Optional, Any


class Tree:
    """A recursive tree data structure, used to represent data from restaurants.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item. Items are sorted in ascending order by root.
    _root: Optional[Any]
    _subtrees: list[Tree]
    rating: Optional[float]
    price: Optional[float]

    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            return 1 + sum(subtree.__len__() for subtree in self._subtrees)

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def add_restaurant(self, info: list[str]) -> None:
        """ Mutates this tree to add given restaurant based on its information

        Preconditions:
            - info is in proper format
        """
        if len(info) == 2:
            self.add_price_rating(float(info[0]), float(info[1]))
        else:
            items = info[len(info) - 1].split(',')
            for item in items:
                tree = None
                for subtree in self._subtrees:
                    if subtree._root == item:
                        tree = subtree

                if tree is None:
                    tree = Tree(item, [])
                    self._subtrees.append(tree)  # TODO: sort it

                tree.add_restaurant(info[:len(info) - 1])

    def add_price_rating(self, price: float, rating: float) -> None:
        """ Mutates this tree to add rating and price

        Preconditions:
            - this tree must be a restaurant name
        """
        self.price = price
        self.rating = rating


class TreeBuilder:
    """ Class used to build the tree from the restaurant data
    """

    def build_tree(self, data: str) -> Tree:
        """ Mutates input tree to add restaurant data
        """
        tree = Tree('root', [])
        with open(data, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if '' not in row:  # does not use restaurants with missing info
                    tree.add_restaurant(row[1:])

        return tree
