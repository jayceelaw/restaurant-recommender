"""Module"""
import tkinter as tk
from tkinter import messagebox

QUESTIONS = ['Budget:', 'How many places do you want to go?',
             'What cuisine', 'Choose:', 'Online ordering?',
             'Table reservation']


def get_user_input(questions: list[str], answers_so_far: []) -> None:
    """Return the user's answers to a list of Yes/No questions."""
    print(questions[0])
    s = input('')
    answers_so_far.append(s)
    print(questions[1])
    k = input('from 1 to 5 :')
    answers_so_far.append(k)
    for i in range(int(k)):
        place = []
        print('Preferences for place ' + str(i + 1))
        for question in questions[2:3]:
            print(question)
            l = input('i.e japanese, chinese, korean, italian')
            place.append(l.capitalize())
        for question in questions[3:4]:
            print(question)
            l = input('Casual Dining, Quick Bites, Cafe, Delivery, Takeout')
            place.append(l)
        for question in questions[4:]:
            print(question)
            j = input('yes/no:')
            place.append(j.capitalize())
        answers_so_far.append(place)
