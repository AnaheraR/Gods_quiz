from tkinter import *
from functools import partial  # To import unwanted windows
import csv
import random
# import re


class Start:

    def __init__(self):

        # initialise variables
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        button_fg = "#000000"
        button_font = ("Georgia", "13", "bold")

        # Set up GUI Frame
        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # heading and brief instructions
        self.intro_heading_label = Label(self.start_frame,
                                         text="Greek/Roman Gods Quiz",
                                         font=("Georgia", "16", "bold"))
        self.intro_heading_label.grid(row=0)

        choose_instructions_txt = "\nIn this quiz you will be given information " \
                                  "on a certain God/Goddess, such as; what they " \
                                  "rule over and whether they are a Minor or Major god," \
                                  " and have to guess the name of the God/Goddess " \
                                  "based on that information.\n\n" \
                                  "To start, please type in the number " \
                                  "of questions you'd like to answer...\n"
        self.choose_instructions_label = Label(self.start_frame,
                                               text=choose_instructions_txt,
                                               wraplength=390, justify="left")
        self.choose_instructions_label.grid(row=1)

        self.questions_choice_frame = Frame(self.start_frame)
        self.questions_choice_frame.grid(row=2)

        self.questions_entry = Entry(self.questions_choice_frame,
                                     font=("Georgia", "14")
                                     )
        self.questions_entry.grid(row=0, column=0, padx=10, pady=10)

        self.output_label = Label(self.questions_choice_frame,
                                  text="", fg="#9C0000")
        self.output_label.grid(row=3)

        self.enter_button = Button(self.questions_choice_frame, text="Enter",
                                   bg="#FFE6CC", fg=button_fg, font=button_font,
                                   width=12, command=self.to_enter)
        self.enter_button.grid(row=0, column=1, padx=10, pady=10)

    def check_rounds(self, min_quest, max_quest):

        has_error = "No"
        error = f"Please enter more than {min_quest} and less than {max_quest} questions.\n" \
                f"No, letters, underscores, spaces, decimals, etc."

        # Check that a valid number has been entered

        response = self.questions_entry.get()

        try:
            response = int(response)

            if response < min_quest:
                has_error = "yes"
            elif response > max_quest:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # Sets var_has_error so that entry box and
        # label can be correctly formatted by formatting function
        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        # if there is no error
        else:
            # set to 'no' in case of previous errors
            self.var_has_error.set("no")
            self.to_quiz(response)

    def to_enter(self):

        to_questions = self.check_rounds(1, 20)

        if to_questions != "invalid":
            self.var_feedback.set("Questions will now start".format(to_questions))

        self.output_answer()

    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()

        if has_errors == "yes":
            # red text, pink entry box
            self.output_label.config(fg="#9C0000")
            self.questions_entry.config(bg="#f8cecc")

        else:
            self.output_label.config(fg="#004C00")
            self.questions_entry.config(bg="#FFFFFF")

        self.output_label.config(text=output)

    def to_quiz(self, num_rounds):
        Quiz(num_rounds)

        # Hide root window
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

        # lists to hold users answer and the correct answers and
        # used to work out statistics
        self.correct_answers = []
        self.incorrect_answers = []

        self.correct_ans = 0
        self.incorrect_ans = 0

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
                                     wraplength=400,
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

        self.correct_answer_label = Label(self.quiz_frame,
                                          text="Correct: 0 \t Incorrect: 0",
                                          fg="#000000", bg="#BAC8D3",
                                          wraplength=300, width=55,
                                          font=("Georgia", "10",))
        self.correct_answer_label.grid(row=4, padx=20, pady=10)

        self.control_frame = Frame(self.quiz_frame)
        self.control_frame.grid(row=5)

        control_buttons = [
            ["#B0E3E6", "Help", "get help"],
            ["#B1E7D0", "Quest Hist", "get stats"],
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

        # disable stats button
        self.to_help_btn = self.control_button_ref[0]
        self.to_stats_btn = self.control_button_ref[1]
        self.to_stats_btn.config(state=DISABLED)

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
            gods_questions = f"Who is the {self.god_info_list[item][0]} god/goddess of {self.god_info_list[item][3]}"
            self.god_naming_info.config(text=gods_questions)

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
        correct_ans = int(self.correct_ans)
        incorrect_ans = int(self.incorrect_ans)

        user_ans = self.answer_entry.get().lower()
        user_ans = user_ans.strip()
        print("You answered", user_ans)
        correct_answer = self.god_info_list[0][2].lower()
        print("The correct answer is", correct_answer)

        self.correct_answers.append(self.correct_answers)
        self.incorrect_answers.append(self.incorrect_answers)

        rounds_choice = self.quest_wanted.get()
        current_quest = self.quest_complete.get()

        end_quiz_label = "Choose - Question {} of {}".format(rounds_choice, rounds_choice)

        if user_ans == correct_answer:
            self.correct_answer_label.config(bg=correct_colour, text=f"Correct: {correct_ans + 1} \t "
                                                                     f"Incorrect: {incorrect_ans}")
            self.correct_ans += 1
        else:
            self.correct_answer_label.config(bg=incorrect_colour, text=f"Correct: {correct_ans} \t "
                                                                       f"Incorrect: {incorrect_ans + 1}")
            self.incorrect_ans += 1

        self.next_question()

        # enable stats button (as we now have at least one question complete)
        self.to_stats_btn.config(state=NORMAL)

        # quest_outcome_txt = "Correct: {} \t Incorrect: {}".format(picked_right)
        # self.correct_answer_label.config(text=quest_outcome_txt)

        if current_quest == rounds_choice:
            # change 'next' button to show overall
            # win / loss result and disable it
            self.naming_heading.config(text=end_quiz_label)
            self.god_naming_info.config(text="Congrats! You finished the quiz.\n"
                                             " Check your History.",
                                        bg="#FFCCE6")
            self.next_enter_button.config(state=DISABLED)

        else:
            # enable next round button and update heading
            self.next_enter_button.config(state="normal")

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats":
            DisplayHist(self, self.correct_answers, self.incorrect_answers)
        else:
            self.close_quiz()

    def close_quiz(self):
        root.deiconify()
        self.quiz_box.destroy()


# show users help / game tips
class DisplayHelp:

    def __init__(self, partner):
        # setup dialogue box and background colour
        background = "#B0E3E6"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_btn.config(state=DISABLED)

        # if users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading_label = Label(self.help_frame, bg=background,
                                        text="Help",
                                        font=("Georgia", "14", "bold"))
        self.help_heading_label.grid(row=0)

        help_text = "Your goal for this quiz is to correctly guess the name of the greek or roman god/goddess " \
                    "that rules over whichever article that you've been given. " \
                    "You will be informed of the god/goddesses ruling " \
                    "and whether they are a greek or roman god, which should help narrow " \
                    "down the possible answers.\n\n" \
                    "Once you answer the question you will immediately move on to the next " \
                    "God/Goddess. You can click the 'Statistics' button to see " \
                    "how many Correct or Incorrect answers you gave. \n\n " \
                    "Good Luck!"
        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left", font=("Georgia", "10"))
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Georgia", "12", "bold"),
                                     text="Dismiss", bg="#0E8088",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        partner.to_help_btn.config(state="normal")
        self.help_box.destroy()


# show users their statistics
class DisplayHist:

    def __init__(self, partner, correct_ans, incorrect_ans):

        # setup dialogue box and background colour
        self.stats_box = Toplevel()

        stats_bg_colour = "#B1E7D0"

        # disable stats button
        partner.to_stats_btn.config(state=DISABLED)

        # if users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200,
                                 bg=stats_bg_colour)
        self.stats_frame.grid()

        self.help_heading_label = Label(self.stats_frame, bg=stats_bg_colour,
                                        text="Statistics",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        stats_text = "Here is your statistics"
        self.stats_text_label = Label(self.stats_frame, bg=stats_bg_colour,
                                      text=stats_text, wraplength=350,
                                      justify="left")
        self.stats_text_label.grid(row=1, padx=10)

        table_heading_txt = "Quest no.     Player answer\t   Correct answer"
        self.table_heading = Label(self.stats_frame, bg="#BFFAE1",
                                   text=table_heading_txt, wraplength=280,
                                   justify="center")
        self.table_heading.grid(row=2, padx=10)

        # frame to hold statistics 'table'
        self.data_frame = Frame(self.stats_frame, bg=stats_bg_colour,
                                borderwidth=1, relief="solid")
        self.data_frame.grid(row=4, padx=10, pady=10)

        # get statistics for the player
        # self.question_no = self.get_stats(quest_wanted, "Question no.")
        self.correct_answers = self.get_stats(correct_answers, "Correct")
        self.incorrect_answers = self.get_stats(incorrect_answers, "Incorrect")

        # background formatting
        table_top = "#BFFAE1"
        row_1 = "#BFFAE1"
        # row_2 = "#BFFAE1"

        row_names = ["", "Total"]
        row_formats = [table_top, row_1]

        # data for labels (one label / sub list)
        all_labels = []

        count = 0
        for item in range(0, len(self.correct_answers)):
            # all_labels.append([f"Question {count + 1}", row_formats[count]])
            all_labels.append([row_names[item], row_formats[count]])
            all_labels.append([correct_ans[item], row_formats[count]])
            all_labels.append([incorrect_ans[item], row_formats[count]])
            count += 1

        # create labels based on list above
        for item in range(0, len(all_labels)):
            self.data_label = Label(self.data_frame, text=all_labels[item][0],
                                    bg=all_labels[item][1], width="10", height="2",
                                    padx=5)
            self.data_label.grid(row=item // 3, column=item % 3,
                                 padx=0, pady=0)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#0E865E",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=5, padx=10, pady=10)

    @staticmethod
    def get_stats(stats_list, entity):

        print("stats list", stats_list)

        totals = sum(stats_list)

        return [entity, totals]

    def close_stats(self, partner):
        partner.to_stats_btn.config(state="normal")
        self.stats_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Greek/Roman Gods Quiz")
    Start()
    root.mainloop()
