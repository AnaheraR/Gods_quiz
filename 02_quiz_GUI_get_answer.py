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

        # stores the god information
        self.god_variable = StringVar()
        self.god_variable.set("")

        # variables used to work out statistics, when game ends etc
        self.quest_wanted = IntVar()
        self.quest_wanted.set(rounds_choice)

        # questions completed
        self.quest_complete = IntVar()
        self.quest_complete.set(0)

        # lists to hold users correct and incorrect answers and
        # used to work out statistics
        self.correct_ans = []
        self.incorrect_ans = []

        # get all the gods info for use in this quiz
        self.gods_info = self.get_gods_info()

        self.quiz_frame = Frame(self.quiz_box, padx=10, pady=10)
        self.quiz_frame.grid()

        rounds_heading = "Question 1 of {}".format(rounds_choice)
        self.naming_heading = Label(self.quiz_frame, text=rounds_heading,
                                    font=("Georgia", "16", "bold")
                                    )
        self.naming_heading.grid(row=0)

        # get god/goddesses info for first round...
        self.god_info_list = []

        self.god_naming_info = Label(self.quiz_frame, width=45, height=2,
                                     fg="#000000", bg="#BAC8D3",
                                     font=("Georgia", "13")
                                     )
        self.god_naming_info.grid(row=1, padx=20, pady=10)

        # self.attempts_label = Label(self.quiz_frame, text="You get three attempts before "
        #                                                  "you must move on.",
        #                            font=("Georgia", "10", "bold")
        #                            )
        # self.attempts_label.grid(row=2)

        # frame for the user to make and enter their guess
        self.guess_frame = Frame(self.quiz_frame)
        self.guess_frame.grid(row=3)

        self.answer_entry = Entry(self.guess_frame,
                                  font=("Georgia", "14"))
        self.answer_entry.grid(row=0, column=0, padx=10, pady=10)

        self.next_enter_button = Button(self.guess_frame, text="Enter",
                                        bg="#FFE6CC", fg="#000000",
                                        font=("Georgia", "13", "bold"),
                                        width=12, command=self.to_compare)
        self.next_enter_button.grid(row=0, column=1, padx=10, pady=10)

        # at the start get a 'new question'
        self.next_question()

        # feedback label under the entry box that lets the user know if there's any errors
        self.answer_feedback_label = Label(self.guess_frame,
                                           text="",
                                           fg="#9c0000",
                                           wraplength=300,
                                           font=("Georgia", "10",))
        self.answer_feedback_label.grid(row=1, column=0, padx=20, pady=10)

        self.correct_answer_label = Label(self.guess_frame,
                                          text="Correct:  \t Incorrect: ",
                                          fg="#000000", bg="#BAC8D3",
                                          wraplength=300,
                                          font=("Georgia", "10",))
        self.correct_answer_label.grid(row=1, column=1, padx=20, pady=10)

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
        completed_quest = []
        # get a god
        while len(god_quest_list) < 1:
            # Choose item
            chosen_god = random.choice(self.gods_info)
            index_chosen = self.gods_info.index(chosen_god)

            # check god has not been given
            if chosen_god[2] not in completed_quest:
                # add item to quest list
                god_quest_list.append(chosen_god)
                completed_quest.append(chosen_god[2])

                # remove item from master list
                self.gods_info.pop(index_chosen)

        return god_quest_list

    def next_question(self):

        # empty list so we can get a new god
        self.god_info_list.clear()

        # get new gods for question
        self.god_info_list = self.get_quest_gods()

        for item in range(1):
            gods_questions = f"Who is the {self.god_info_list[item][0]} god of {self.god_info_list[item][3]}"
            self.god_naming_info.config(text=gods_questions)

        correct_ans = self.god_info_list[0][2]
        print("The correct answer is", correct_ans)

        # retrieve number of questions wanted / played
        # and update heading.
        rounds_choice = self.quest_wanted.get()
        current_quest = self.quest_complete.get()
        current_quest += 1
        self.quest_complete.set(current_quest)
        new_heading = "Choose - Question {} of " \
                      "{}".format(current_quest, rounds_choice)
        self.naming_heading.config(text=new_heading)

    def to_compare(self):

        correct_colour = "#D5E8D4"
        incorrect_colour = "#F8CECC"

        # picked_right = self.correct_ans

        user_ans = self.answer_entry.get()
        correct_answer = self.god_info_list[0][2]
        rounds_choice = self.quest_wanted.get()
        current_quest = self.quest_complete.get()

        end_quiz_label = "Choose - Question {} of {}".format(rounds_choice, rounds_choice)

        if user_ans == correct_answer:
            self.correct_answer_label.config(bg=correct_colour)
        else:
            self.correct_answer_label.config(bg=incorrect_colour)

        self.next_question()

        # quest_outcome_txt = "Correct: {} \t Incorrect: {}".format(picked_right)
        # self.correct_answer_label.config(text=quest_outcome_txt)

        if current_quest == rounds_choice:
            # change 'next' button to show overall
            # win / loss result and disable it
            self.naming_heading.config(text=end_quiz_label)
            self.god_naming_info.config(text="Congrats! You finished the quiz.\n"
                                             " Check your Statistics.",
                                        bg="#FFCCE6")
            self.next_enter_button.config(state=DISABLED)

        else:
            # enable next round button and update heading
            self.next_enter_button.config(state="normal")

    @staticmethod
    def answer_error(answer):
        problem = ""

        # regular expression to check entry is valid
        valid_char = "[A-Za-z ]"

        # iterates through entry and checks each letter.
        for letter in answer:
            if re.match(valid_char, letter):
                continue

            elif letter:
                problem = ("Sorry, no {}'s allowed".format(letter))
            break

        if problem != "":
            problem = "{}.  Use letters only.".format(problem)

        return problem

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
