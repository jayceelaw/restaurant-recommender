""" CSC111 Project 2: Restaurant Recommendation System

Module Description
==================
This module contains the Tree and TreeBuilder classes to build the
tree from the data set.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 UofT DCS Teaching Team """

from __future__ import annotations

import csv
from typing import Optional, Any


class Tree:
    """A recursive tree data structure, used to represent data from restaurants.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - self.rating >= 0
        - self.price >= 0

    Instance Attributes:
        - root: The item stored at this tree's root, or None if the tree is empty.
        - subtrees: The list of subtrees of this tree. This attribute is empty when
                    self._root is None (representing an empty tree). However, this attribute
                    may be empty when self._root is not None, which represents a tree consisting
                    of just one item. Items are sorted in ascending order by root.
        - rating: average rating (out of 5) for the restaurant
        - price: average price (for 2 people) for the restaurant
        - og_index: original index of the restaurant in the csv file
    """
    _root: Optional[Any]
    _subtrees: list[Tree]
    rating: Optional[float]
    price: Optional[float]
    og_index: Optional[int]

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
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def __repr__(self) -> str:
        """Return a one-line string representation of this tree.

        >>> t = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> t
        Tree(2, [Tree(4, []), Tree(5, [])])
        """
        if self.is_empty():
            return 'Tree(None, [])'
        else:
            subtrees = []
            for subtree in self._subtrees:
                subtrees.append(repr(subtree))

            return f'Tree({self._root}, [{", ".join(subtrees)}])'

    def add_restaurant(self, info: list[str], i: int) -> None:
        """ Mutates this tree to add given restaurant based on its information.

        Recursively adds each subsequent piece of information as a child of the
        previous (in the order cuisine -> type -> table booking -> online order)
        and adds the price/rating/index to the restaurant name.

        Preconditions:
            - info is in proper format
        """
        if len(info) == 2:
            self.add_price_rating(float(info[0]), float(info[1]))
            self.og_index = i
        else:
            items = info[len(info) - 1].split(',')
            for item in items:
                self._add_restaurant_helper(info, i, item.lstrip())

    def _add_restaurant_helper(self, info: list[str], i: int, item: str) -> None:
        """ Helper method for add_restaurant().
        """
        tree = None
        for subtree in self._subtrees:
            if subtree._root == item:
                tree = subtree

        if tree is None:
            tree = Tree(item, [])
            self.insert_tree(tree)

        tree.add_restaurant(info[:len(info) - 1], i)

    def add_price_rating(self, price: float, rating: float) -> None:
        """ Mutates this tree to add rating and price.

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

    def find_restaurants(self, user_input: list[str]) -> Optional[set[Tree]]:
        """Returns a set of all restaurants matching user input for each category,
        or None if there are no matches.

        Uses binary search on sorted subtrees to find matches.

        Preconditions:
         - user_input in correct format:
            [cuisine, type, table booking, online order]
         - self._subtrees is sorted
        """
        # base case - return list of restaurants
        if len(user_input) == 0:
            return set(self._subtrees)
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

            return None

    def filter_restaurants(self, num_places: int, max_budget: int, user_input: list) -> Optional[list[int]]:
        """Returns a list of the indices of the restaurants whose total average prices fall within
        the max_budget, including all cuisines listed in user_input.

        Preconditions:
            - all(r.rating is not None and r.price is not None for r in restaurants)
            - 0 <= max_budget
            - len(user_input[0]) <= num_places
            - user_input in the form [{cuisines}, type, table booking, online order]
            - self._root == 'root'
        """
        budget = max_budget / num_places
        all_restaurants = []

        for cuisine in user_input[0]:
            restaurants = self.find_restaurants([cuisine] + user_input[1:])
            if restaurants is not None:
                restaurants = [r for r in restaurants if r.price <= budget]
                restaurants.sort(key=lambda r: r.rating, reverse=True)
                all_restaurants.append(restaurants)

        if all_restaurants:
            selected = [rts[0].og_index for rts in all_restaurants if rts]
            all_restaurants = [restaurant for rts in all_restaurants for restaurant in rts if
                               restaurant.og_index not in selected]
            return selected + [restaurant.og_index for restaurant in all_restaurants[:num_places - len(selected)]]
        else:
            return None

    def get_all_cuisines(self) -> list[str]:
        """ Returns a list of all cuisines in tree (sorted in alphabetical order).

        Preconditions:
            - self._root == 'root'
        """
        cuisines = []
        for cuisine in self._subtrees:
            cuisines.append(cuisine._root)

        return cuisines

    def get_all_types(self) -> list[str]:
        """ Returns a list of all types in tree.

        Preconditions:
            - self._root == 'root'
        """
        types = set()
        for cuisine in self._subtrees:
            for res_type in cuisine._subtrees:
                types.add(res_type._root)

        return list(types)

    def get_restaurant_info(self, restaurant_indices: list[int], tree_builder: TreeBuilder) -> list[tuple]:
        """ Returns a list of tuples with each corresponding restaurant and their information
        based on the indices in restaurant_indices in the form:
            (name, cuisines, types, rating, average price)

        Preconditions:
            - all(0 <= i <= 7104 for i in restaurant_indices)
        """
        infos = []
        for i in restaurant_indices:
            info = tuple(tree_builder.get_info(i))
            infos.append((info[2], info[6], info[5], info[1], info[0]))
        return infos


class TreeBuilder:
    """Class used to build the tree from the restaurant data.

     Instance Attributes:
        - data: csv file name of restaurant dataset
    """
    data: str

    def __init__(self, data: str) -> None:
        """Initialize a new TreeBuilder with the given data.
        """
        self.data = data

    def build_tree(self) -> Tree:
        """Creates tree representing restaurant dataset.
        """
        tree = Tree('root', [])
        with open(self.data, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if '' not in row:  # does not use restaurants with missing info
                    # converts indian rupees to canadian dollars for tree
                    tree.add_restaurant([str(self.inr_to_cad(float(row[1])))] + row[2:], int(row[0]))

        return tree

    def get_info(self, i: int) -> Optional[list[str]]:
        """ Returns a list of corresponding information to restaurant, based on its index.
        """
        with open(self.data, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != '' and i == int(row[0]):
                    return [str(self.inr_to_cad(float(row[1])))] + row[2:]

            return None

    def inr_to_cad(self, amount: float) -> float:
        """ Converts amount (given in Indian rupees) to Canadian dollars.
        Exchange rate as of March 30, 2024.
        """
        return round(amount * 0.016, 1)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    # python_ta.check_all('functions.py', config={
    #     'max-line-length': 120,
    #     'extra-imports': ['__future__', 'typing', 'csv'],
    #     'allowed-io': ['TreeBuilder.build_tree', 'TreeBuilder.get_info']
    # })
