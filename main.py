""" TODO: docstring """
import python_ta

from assignments.project2.functions import TreeBuilder

t = TreeBuilder()
tree = t.build_tree('test_data.csv')
print(tree)

print(tree.find_restaurants(['Beverages', 'Dessert Parlor', 'No', 'Yes']))


python_ta.check_all(config={
    'extra-imports': [],  # the names (strs) of imported modules
    'allowed-io': [],     # the names (strs) of functions that call print/open/input
    'max-line-length': 120
})
