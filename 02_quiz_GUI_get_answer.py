from tkinter import *
from functools import partial  # To import unwanted windows
import csv
import random
import re


class Start:

    def __init__(self):
        # invoke play class with three rounds for testing purposes
        self.to_quiz(3)

    def to_quiz(self, num_rounds):
        Quiz(num_rounds)

        # Hide root window (ie: hide rounds choice window)
        root.withdraw()


class Quiz:

    def __init__(self, rounds_choice):
        self.quiz_box = Toplevel()
        # if users press cross at top, closes
        # the box
        self.quiz_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_quiz))

        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        # variables used to work out statistics, when game ends etc
        self.quest_wanted = IntVar()
        self.quest_wanted.set(rounds_choice)

        # initially set rounds played and rounds won to 0
        self.quest_complete = IntVar()
        self.quest_complete.set(0)

        self.correct_ans = []

        # get all the gods info for use in this quiz
        self.gods_info = self.get_gods_info()

        self.quiz_frame = Frame(self.quiz_box, padx=10, pady=10)
        self.quiz_frame.grid()

        rounds_heading = "Question 1 of {}".format(rounds_choice)
        self.naming_heading = Label(self.quiz_frame, text=rounds_heading,
                                    font=("Georgia", "16", "bold")
                                    )
        self.naming_heading.grid(row=0)

        self.god_info_list = []
        self.god_info_ref = []

        self.god_info = Label(self.quiz_frame, width=35, height=2,
                              text="Who is the {} god of {}",
                              fg="#000000", bg="#BAC8D3",
                              font=("Georgia", "13"))
        self.god_info_ref.append(self.god_info)
        self.god_info.grid(row=1, padx=20, pady=10)

        self.attempts_label = Label(self.quiz_frame, text="You get three attempts before "
                                                          "you must move on.",
                                    font=("Georgia", "10", "bold")
                                    )
        self.attempts_label.grid(row=2)

        self.guess_frame = Frame(self.quiz_frame)
        self.guess_frame.grid(row=3)

        self.answer_entry = Entry(self.guess_frame,
                                  font=("Georgia", "14"))
        self.answer_entry.grid(row=0, column=0, padx=10, pady=10)

        self.next_enter_button = Button(self.guess_frame, text="Enter",
                                        bg="#FFE6CC", fg="#000000",
                                        font=("Georgia", "13", "bold"),
                                        width=12)
        self.next_enter_button.grid(row=0, column=1, padx=10, pady=10)

        self.next_question()

        self.answer_feedback_label = Label(self.guess_frame,
                                           text="",
                                           fg="#9c0000",
                                           wraplength=300,
                                           font=("Georgia", "10",))
        self.answer_feedback_label.grid(row=1)

        self.control_frame = Frame(self.quiz_frame)
        self.control_frame.grid(row=4)

        control_buttons = [
            ["#B0E3E6", "Help", "get help"],
            ["#B1E7D0", "Statistics", "get stats"],
            ["#E0B1E7", "Start Over", "start over"]
        ]

        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#000000",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Georgia", "12"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # add buttons to control list
            self.control_button_ref.append(self.make_control_button)

    def get_gods_info(self):
        file = open("gods.csv", "r")
        var_all_gods = list(csv.reader(file, delimiter=","))
        file.close()

        var_all_gods.pop(0)
        return var_all_gods

    def get_quest_gods(self):
        god_quest_list = []

        # get six unique colours
        while len(god_quest_list) < 1:
            # Choose item
            chosen_god = random.choice(self.gods_info)
            index_chosen = self.gods_info.index(chosen_god)

            # check score is not already in list
            if chosen_god[1]:
                # add item to rounds list
                god_quest_list.append(chosen_god)

                # remove item from master list
                self.gods_info.pop(index_chosen)

        return god_quest_list

    def next_question(self):

        # empty button list so we can get new colours
        self.god_info_list.clear()

        # get new colours for buttons
        self.god_info_list = self.get_quest_gods()

        count = 0
        for item in self.god_info_ref:
            item['god_origin'] = self.god_info_list[count][0]
            item['god_ruling'] = self.god_info_list[count][3]

        # retrieve number of rounds wanted / played
        # and update heading.
        rounds_choice = self.quest_wanted.get()
        current_quest = self.quest_complete.get()
        new_heading = "Choose - Round {} of " \
                      "{}".format(current_quest + 1, rounds_choice)
        self.naming_heading.config(text=new_heading)

    def check_answer(self, user_choice):

        rounds_choice = self.quest_wanted.get()

        current_quest = self.quest_complete.get()
        current_quest += 1
        self.quest_complete.set(current_quest)

        to_remove = self.god_info_list.index(user_choice)
        self.god_info_list.pop(to_remove)



    @staticmethod
    def answer_error(answer):
        problem = ""

        # regular expression to check filename is valid
        valid_char = "[A-Za-z]"

        # iterates through filename and checks each letter.
        for letter in answer:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "Sorry, no spaces allowed"

            else:
                problem = ("Sorry, no {}'s allowed".format(letter))
            break

        if problem != "":
            problem = "{}.  Use letters only.".format(problem)

        return problem

    def to_next_quest(self):

        to_next_question = self.answer_error()

        if to_next_question != "problem":
            self.var_feedback.set("Questions will now start".format(to_next_question))

        self.answer_error()

    def to_do(self, action):
        if action == "get help":
            self.get_help()
        elif action == "get stats":
            self.get_stats()
        else:
            self.close_quiz()

    def get_stats(self):
        print("You choose to get the statistics")

    def get_help(self):
        print("You choose to get help")

    def close_quiz(self):
        root.deiconify()
        self.quiz_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Greek/Roman Gods Quiz")
    Start()
    root.mainloop()
