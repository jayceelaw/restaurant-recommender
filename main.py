""" TODO: docstring """
import python_ta

from functions import TreeBuilder
from recommendation_system import get_user_input
QUESTIONS = ['Budget:', 'How many places do you want to go?',
             'What cuisine', 'Choose:', 'Online ordering?',
             'Table reservation']


t = TreeBuilder()
tree = t.build_tree('data.csv')
# print(tree)
answer = []
get_user_input(QUESTIONS, answer)

lits_of_sets = tree.restaurant_combination(answer)

print(tree.find_combinations(lits_of_sets, int(answer[0]))[:5])


python_ta.check_all(config={
    'extra-imports': [],  # the names (strs) of imported modules
    'allowed-io': [],     # the names (strs) of functions that call print/open/input
    'max-line-length': 120
})
