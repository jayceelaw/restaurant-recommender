""" CSC111 Project 2: Restaurant Recommendation System

Module Description
==================
This module contains RestaurantSelector class which uses tkinter to display
the user interface to choose preferences for restaurants.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 UofT DCS Teaching Team """

import tkinter as tk
from tkinter import ttk, messagebox
from functions import Tree, TreeBuilder


class RestaurantSelector:
    """Class representing user interface to select and display restaurant
    recommendations (using tkinter)

    Representation Invariants:
        - self.tree._root == 'root'

    Instance Attributes:
        - master: master for user interface display, using tkinter
        - tree: tree representing dataset of restaurants
        - t: tree builder to access certain methods with the tree
        - cuisine_list: list of all cuisines in dataset
        - types_list: list of all restaurant types in dataset
        - budget: user input for total maximum budget
        - num_places: user input for number of places they want to go
        - cuisines: user input for list of cuisines they want to eat
        - restaurant_type: user input for type of restaurant they want
        - online_order: user input for whether they want online ordering
        - table_booking: user input for whether they want table booking
    """
    master: tk.Tk
    tree: Tree
    t: TreeBuilder
    cuisine_list: list[str]
    types_list: list[str]
    budget: tk.StringVar
    num_places: tk.IntVar
    cuisines: list[str]
    restaurant_type: tk.StringVar
    online_order: tk.BooleanVar
    table_booking: tk.BooleanVar
    cuisine_listbox: tk.Listbox
    cuisines_label: tk.Label

    def __init__(self, master: tk.Tk, tree: Tree, t: TreeBuilder) -> None:
        """Initialize a new RestaurantSelector with the given master (tkinter),
        tree dataset, and tree builder.

        Calls display_input() to create the window for the initial user interface.
        """
        self.master = master
        self.master.title("Restaurant Selector")
        self.master.geometry("500x500")

        self.tree = tree
        self.t = t
        self.cuisine_list = tree.get_all_cuisines()
        self.types_list = tree.get_all_types()

        # variables for user input
        self.budget = tk.StringVar()
        self.num_places = tk.IntVar()
        self.cuisines = []
        self.restaurant_type = tk.StringVar()
        self.online_order = tk.BooleanVar()
        self.table_booking = tk.BooleanVar()

        self.display_input()

    def display_input(self) -> None:
        """Uses the tkinter library to create and display a window showing all
        the categories for user input, and a submit button to run the program
        to find restaurant recommendations.

        Allows users to input their budget, number of times they want to go out,
        select multiple cuisines and 1 type from the list, and checkboxes for
        whether they want table booking and online ordering options.

        Updates variables to store user input.
        """
        # budget input
        budget_frame = ttk.Frame(self.master)
        budget_frame.pack(pady=10)
        ttk.Label(budget_frame, text="Budget/Meal Plan:").grid(row=0, column=0)
        budget_entry = ttk.Entry(budget_frame, textvariable=self.budget)
        budget_entry.grid(row=0, column=1)

        # number of times to go out
        num_places_frame = ttk.Frame(self.master)
        num_places_frame.pack(pady=10)
        ttk.Label(num_places_frame, text="Number of times to go out:").grid(row=0, column=0)
        num_places_spinbox = ttk.Spinbox(num_places_frame, from_=1, to=10, textvariable=self.num_places,
                                         state="readonly")
        num_places_spinbox.grid(row=0, column=1)

        # cuisine selection
        cuisine_frame = ttk.Frame(self.master)
        cuisine_frame.pack(pady=10)
        ttk.Label(cuisine_frame, text="Select cuisines:").grid(row=0, column=0)
        cuisine_entry = ttk.Entry(cuisine_frame)
        cuisine_entry.grid(row=0, column=1)
        cuisine_entry.bind('<KeyRelease>', lambda event: self.check_key(cuisine_entry))
        self.cuisine_listbox = tk.Listbox(cuisine_frame, height=5, selectmode='single')
        self.cuisine_listbox.grid(row=1, column=0, columnspan=2)
        add_cuisine_button = ttk.Button(cuisine_frame, text="Add", command=self.add_cuisine)
        add_cuisine_button.grid(row=0, column=2)
        delete_cuisine_button = ttk.Button(cuisine_frame, text="Delete", command=self.delete_cuisine)
        delete_cuisine_button.grid(row=1, column=2)
        self.cuisines_label = ttk.Label(cuisine_frame, text="Selected Cuisines:")
        self.cuisines_label.grid(row=2, column=0, columnspan=3)

        # restaurant type selection
        restaurant_frame = ttk.Frame(self.master)
        restaurant_frame.pack(pady=10)
        ttk.Label(restaurant_frame, text="Select restaurant type:").grid(row=0, column=0)
        restaurant_combobox = ttk.Combobox(restaurant_frame, textvariable=self.restaurant_type,
                                           values=self.types_list, state="readonly")
        restaurant_combobox.grid(row=0, column=1)

        # online ordering selection
        online_order_frame = ttk.Frame(self.master)
        online_order_frame.pack(pady=10)
        ttk.Checkbutton(online_order_frame, text="Online Ordering", variable=self.online_order).grid(row=0, column=0)

        # table booking selection
        table_booking_frame = ttk.Frame(self.master)
        table_booking_frame.pack(pady=10)
        ttk.Checkbutton(table_booking_frame, text="Table Booking", variable=self.table_booking).grid(row=0, column=0)

        # submit
        ttk.Button(self.master, text="Submit", command=self.submit).pack(pady=10)

    def check_key(self, cuisine_entry: ttk.Entry) -> None:
        """Adds cuisine_entry to the displayed list of cuisines chosen.
        """
        value = cuisine_entry.get().strip()
        data = []
        if value:
            for item in self.cuisine_list:
                if value.lower() in item.lower():
                    data.append(item)
        else:
            data = self.cuisine_list
        self.update(data)

    def update(self, data: list[str]) -> None:
        """Updates the displayed list of cuisines with the provided data
        """
        self.cuisine_listbox.delete(0, 'end')
        for item in data:
            self.cuisine_listbox.insert('end', item)

    def add_cuisine(self) -> None:
        """Add the selected cuisine from the listbox to the list of selected cuisines.

        If a cuisine is selected in the listbox, and it's not already in the list of selected cuisines,
        add it to the list and update the display of selected cuisines.
        """
        selected_index = self.cuisine_listbox.curselection()
        if selected_index:
            cuisine = self.cuisine_listbox.get(selected_index[0])
            if cuisine not in self.cuisines:
                self.cuisines.append(cuisine)
            self.update_selected_cuisines()

    def delete_cuisine(self) -> None:
        """Delete the last added cuisine from the list of selected cuisines, if any.
        """
        if self.cuisines:
            self.cuisines.pop()
            self.update_selected_cuisines()

    def update_selected_cuisines(self) -> None:
        """Update the display of selected cuisines label with the current list of selected cuisines.
        """
        self.cuisines_label.config(text="Selected Cuisines: " + ", ".join(self.cuisines))

    def validate_input(self) -> bool:
        """Checks user input to see if its valid and returns True if it is, False otherwise.

        Displays error message showing error if there is any.
        """
        # required fields are empty
        if self.budget.get().strip() == '' or not self.cuisines or self.restaurant_type.get().strip() == '':
            messagebox.showerror("Error", "Please fill out all the required fields.", parent=self.master)
            return False
        # budget is not an integer
        elif not self.budget.get().isdigit():
            messagebox.showerror("Error", "Budget must be an integer.", parent=self.master)
            return False
        # 0 number of places chosen to go
        elif self.num_places.get() == 0:
            messagebox.showerror("Error", "Please choose 1-10 number of places to go.", parent=self.master)
            return False
        # too many cuisines chosen
        elif len(self.cuisines) > self.num_places.get():
            messagebox.showerror("Error", f"Too many cuisines chosen, please only choose up to "
                                          f"{self.num_places.get()} cuisine(s)", parent=self.master)
            return False

        return True

    def display_results(self, results: list[tuple]) -> None:
        """Creates a pop-up window showing table of matching restaurants with
        their corresponding information.

        Preconditions:
            - results is in the correct format:
                [(name, cuisines, types, rating, average price), ...]
        """
        popup = tk.Toplevel()
        popup.title("Results")

        # create treeview widget
        treeview = ttk.Treeview(popup)
        treeview["columns"] = ("Cuisine", "Type", "Rating", "Average Price")
        treeview.heading("#0", text="Restaurant Name")
        treeview.heading("Cuisine", text="Cuisine")
        treeview.heading("Type", text="Type")
        treeview.heading("Rating", text="Rating")
        treeview.heading("Average Price", text="Average Price")

        # setting the widths for the last 2 colummns
        treeview.column("Rating", anchor="w", width=75)
        treeview.column("Average Price", anchor="w", width=75)

        for data in results:
            treeview.insert("", "end", text=data[0], values=data[1:])

        treeview.pack(expand=True, fill="both")

    def submit(self) -> None:
        """Checks if user input is valid, then calls the filter_restaurants() function to find
        matching restaurant recommendations based on the user input.

        If there are matching results, it displays it using display_results() to the user. If not,
        it shows a message box telling the user that there are no matches.
        """
        if self.validate_input():
            # retrieve and process user input
            budget = int(self.budget.get())
            num_places = self.num_places.get()
            restaurant_type = self.restaurant_type.get()
            online_order = self.online_order.get()
            table_booking = self.table_booking.get()

            results = self.tree.filter_restaurants(num_places, budget, [set(self.cuisines), restaurant_type,
                                                                        'Yes' if table_booking else 'No',
                                                                        'Yes' if online_order else 'No'])

            if results:
                self.display_results(self.tree.get_restaurant_info(results, self.t))
            else:
                messagebox.showinfo("Restaurants", 'Sorry, there were no matching restaurants')


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    # python_ta.check_all('user_interface.py', config={
    #     'max-line-length': 120,
    #     'extra-imports': ['tkinter', 'functions'],
    #     'allowed-io': []
    # })
