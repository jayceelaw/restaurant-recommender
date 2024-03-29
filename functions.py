""" TODO: docstring """

from __future__ import annotations

import csv
from typing import Optional, Any


class Tree:
    """A recursive tree data structure, used to represent data from restaurants.

    Representation Invariants:
        - self._root is not None or self._subtrees == []

    Instance Attributes:
        - root: The item stored at this tree's root, or None if the tree is empty.
        - subtrees: The list of subtrees of this tree. This attribute is empty when
                    self._root is None (representing an empty tree). However, this attribute
                    may be empty when self._root is not None, which represents a tree consisting
                    of just one item. Items are sorted in ascending order by root.
    """

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
                    if subtree._root == item.lstrip():
                        tree = subtree

                if tree is None:
                    tree = Tree(item.lstrip(), [])
                    self.insert_tree(tree)

                tree.add_restaurant(info[:len(info) - 1])

    def add_price_rating(self, price: float, rating: float) -> None:
        """ Mutates this tree to add rating and price

        Preconditions:
            - this tree must be a restaurant name
        """
        self.price = price
        self.rating = rating

    def insert_tree(self, tree: Tree) -> None:
        """ Mutates this tree to add tree to subtrees while keeping it sorted.

        Preconditions:
            - self._subtrees is sorted

        >>> t = Tree('root', [Tree(1, []), Tree(2, []), Tree(4, [])])
        >>> t.insert_tree(Tree(3, []))
        >>> t._subtrees
        [Tree(1, []), Tree(2, []), Tree(3, []), Tree(4, [])]
        """
        if len(self._subtrees) == 0:
            self._subtrees.append(tree)
        else:
            for i in range(len(self._subtrees)):
                if self._subtrees[i]._root > tree._root:
                    self._subtrees.insert(i, tree)
                    return
            self._subtrees.append(tree)

    def find_restaurants(self, user_input: list[str]) -> set[str]:
        """
        Returns a set of all restaurants matching user input for each category,
        or None if there are no matches.

        Preconditions:
         - user_input in correct format ([cuisine, type, table booking, online order])
        """
        # base case - return list of restaurants
        if len(user_input) == 0:
            return {subtree._root for subtree in self._subtrees}
        else:
            start = 0
            end = len(self._subtrees)

            while start < end:
                mid = (start + end) // 2
                mid_subtree = self._subtrees[mid]

                if user_input[0] == mid_subtree._root:
                    # recursively search on matching subtree
                    return mid_subtree.find_restaurants(user_input[1:])
                elif user_input[0] < mid_subtree._root:
                    end = mid
                else:
                    start = mid + 1

    def restaurant_combination(self, user_info: list) -> list[set]:
        """ Find combinations of restaurant based on the user's input"""
        places = []
        for place in user_info[2:]:
            match = self.find_restaurants(place)
            places.append(match)
        if None in places:
            print('No match found')
        return places

    def find_leaf_node(self, target: str) -> Optional[Tree]:
        """ Find restaurant with gviven name"""
        if self._root == target:
            return self

        for subtree in self._subtrees:
            result = subtree.find_leaf_node(target)
            if result:
                return result

        return None

    def find_combinations(self, list_of_sets: list[set], budget: int):
        """
        Preconditions:
        - list_of_sets is not None
        """
        def generate_combinations(index, current_combination, current_price):
            if current_price > budget:
                return []

            if index == len(list_of_sets):
                return [current_combination]

            combinations = []
            for leaf in list_of_sets[index]:
                new_combination = current_combination + [leaf]
                new_price = current_price + self.find_leaf_node(leaf).price
                combinations.extend(generate_combinations(index + 1, new_combination, new_price))

            return combinations

        return generate_combinations(0, [], 0)


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
