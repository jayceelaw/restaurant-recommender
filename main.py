""" CSC111 Project 2: Restaurant Recommendation System

Module Description
==================
This module contains the main block of code to run the restaurant
recommendation program.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 UofT DCS Teaching Team """

import tkinter as tk
from functions import TreeBuilder
from user_interface import RestaurantSelector

t = TreeBuilder('data.csv')
tree = t.build_tree()

root = tk.Tk()
app = RestaurantSelector(root, tree, t)

# Uncomment these 2 lines to try the sample output (as shown in the report) for these inputs
# results = tree.filter_restaurants(6, 100, [{'Mexican', 'Chinese', 'North Indian'}, 'Casual Dining', 'Yes', 'No'])
# app.display_results(tree.get_restaurant_info(results, t))

root.mainloop()
