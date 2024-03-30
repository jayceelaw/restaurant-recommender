"""Module"""

from tkinter import ttk
import tkinter as tk

# Define a global variable to hold the collected input
preferences_data = None


def get_user_input():
    """ Get user input using tkinter library"""
    window = tk.Tk()
    window.title("Meal Plan Recommendation")
    answer = []

    def create_preference_fields():
        """ Get preference for each place"""
        # Function to create preference fields based on user input
        user_input = number_combobox.get()
        j = 5

        for i in range(1, int(user_input) + 1):
            place = []
            if i % 2 == 0:
                title = "Preferences for place " + str(i)
                frames = tk.LabelFrame(frame, text=title)
                frames.grid(row=j, column=1)
                cuisine_frame = tk.Label(frames, text="Which cuisine?")
                cuisine_frame.grid(row=j + 1, column=1)
                cuisine_entry = tk.Entry(frames)
                cuisine_entry.grid(row=j + 2, column=1)

                type_frame = tk.Label(frames, text="What type?")
                type_frame.grid(row=j + 3, column=1)
                type_combobox = ttk.Combobox(frames,
                                             values=['Casual Dining', 'Quick Bites', 'Cafe', 'Takeaway', 'Delivery'])
                type_combobox.grid(row=j + 4, column=1)

                online_order_var = tk.StringVar(value="No")
                checkbox1 = tk.Checkbutton(frames, text="Online ordering", variable=online_order_var, onvalue="Yes",
                                           offvalue="No")
                checkbox1.grid(row=j + 5, column=1)

                table_reserve_var = tk.StringVar(value="No")
                checkbox = tk.Checkbutton(frames, text="Table reserve", variable=table_reserve_var, onvalue="Yes",
                                          offvalue="No")
                checkbox.grid(row=j + 6, column=1)
                answer.append([cuisine_entry, type_combobox, online_order_var, table_reserve_var])

                j += 7

            else:
                title = "Preferences for place " + str(i)
                frames = tk.LabelFrame(frame, text=title)
                frames.grid(row=j, column=0)
                cuisine_frame = tk.Label(frames, text="Which cuisine?")
                cuisine_frame.grid(row=j + 1, column=0)
                cuisine_entry = tk.Entry(frames)
                cuisine_entry.grid(row=j + 2, column=0)

                type_frame = tk.Label(frames, text="What type?")
                type_frame.grid(row=j + 3, column=0)
                type_combobox = ttk.Combobox(frames, values=['Casual Dining', 'Quick Bites', 'Cafe', 'Takeaway', 'Delivery'])
                type_combobox.grid(row=j + 4, column=0)

                online_order_var = tk.StringVar(value="No")
                checkbox1 = tk.Checkbutton(frames, text="Online ordering", variable=online_order_var, onvalue="Yes",
                                           offvalue="No")
                checkbox1.grid(row=j + 5, column=0)

                table_reserve_var = tk.StringVar(value="No")
                checkbox = tk.Checkbutton(frames, text="Table reserve", variable=table_reserve_var, onvalue="Yes",
                                          offvalue="No")
                checkbox.grid(row=j + 6, column=0)
                answer.append([cuisine_entry, type_combobox, online_order_var, table_reserve_var])

    def submit_preferences():
        """Submit the preference after the button clicked"""
        global preferences_data
        budget = budget_entry.get()
        number = number_combobox.get()
        preferences = [budget, number]
        for place in answer:
            cuisine = place[0].get()
            food_type = place[1].get()
            online_order = place[2].get()
            table_reserve = place[3].get()
            preferences.append([cuisine, food_type, online_order, table_reserve])

        preferences_data = preferences  # Store collected input in global variable
        window.destroy()

    frame = tk.Frame(window)
    frame.pack()

    budget_frame = tk.Label(frame, text="Budget")
    budget_frame.grid(row=0, column=0)
    budget_entry = tk.Entry(frame)
    budget_entry.grid(row=1, column=0)

    number_frame = tk.Label(frame, text="How many places do you want to go?")
    number_frame.grid(row=2, column=0)
    number_combobox = ttk.Combobox(frame, values=['1', '2', '3', '4'])
    number_combobox.grid(row=3, column=0)

    create_button = tk.Button(frame, text="Create Preference Fields", command=create_preference_fields)
    create_button.grid(row=4, column=0)
    submit_button = tk.Button(frame, text="Submit", command=submit_preferences)
    submit_button.grid(row=15, column=0)

    window.mainloop()


# Call the function to start the GUI
def run_user_input():
    """omiited"""
    get_user_input()
    if preferences_data is not None:
        print("Collected input:", preferences_data)
    else:
        print("No input collected.")
