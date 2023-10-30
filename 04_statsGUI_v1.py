from tkinter import *
from functools import partial  # To import unwanted windows
import csv
import random


# users choose 3, 5 or 10 rounds
class ChooseRounds:

    def __init__(self):
        # invoke play class with three rounds for testing purposes
        self.to_play(3)

    def to_play(self, num_rounds):
        Quiz(num_rounds)

        # hide root window (ie: hide rounds choice window)
        root.withdraw()


class Quiz:

    def __init__(self, how_many):

        self.quiz_box = Toplevel()

        self.god_ruling_given = ["harvest", "procreation", "prosperity", "love", "sleep"]
        self.player_answer = ["my ancestor", "my step mother", "Alice", "cupid", "somnus"]
        self.correct_god = ["ceres", "phanes", "abundantia", "cupid", "somnus"]

        self.quiz_frame = Frame(self.quiz_box, padx=10, pady=10)
        self.quiz_frame.grid()

        self.control_frame = Frame(self.quiz_frame)
        self.control_frame.grid(row=5)

        control_buttons = [
            ["#B0E3E6", "Help", "get help"],
            ["#B1E7D0", "Quest Hist", "get stats"],
            ["#E0B1E7", "Start Over", "start over"]
        ]

        # list to hold the references for control buttons
        # so that the text of the 'start over' button can
        # easily be configured when the quiz is over
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
        self.to_stats_btn = self.control_button_ref[1]

    def to_do(self, action):

        if action == "get help":
            pass
        elif action == "get stats":
            DisplayHist(self, self.god_ruling_given, self.player_answer, self.correct_god)
        else:
            self.close_play()

    # DON'T USE THIS FUNCTION IN BASE AS IT KILLS THE ROOT
    def close_play(self):
        root.destroy()


# show users their statistics
class DisplayHist:

    def __init__(self, partner, god_ruling_given, player_answer, correct_god):

        # setup dialogue box and background colour
        self.stats_box = Toplevel()

        # question_num = 1
        # god_question = ""
        # for item in player_answer:
        #     god_question += f"Quest"

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
                                        text="Question History",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        stats_text = "Here is your question history"
        self.stats_text_label = Label(self.stats_frame, bg=stats_bg_colour,
                                      text=stats_text, wraplength=350,
                                      justify="center")
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
        # self.god_stats = self.get_stats(god_ruling_given, "God ruling")
        self.player_stats = self.get_stats(player_answer, "Player answer")
        self.correct_answer_stats = self.get_stats(correct_god, "Correct answer")

        # background formatting 
        table_top = "#BFFAE1"
        row_1 = "#BFFAE1"
        row_2 = "#BFFAE1"

        row_formats = [table_top, row_1, row_2, row_1, row_2]

        # data for labels (one label / sub list)
        all_labels = []

        count = 0
        for item in range(0, len(self.player_stats)):
            all_labels.append([f"Question {count + 1}", row_formats[count]])
            # all_labels.append([self.player_stats[item], row_formats[count]])
            all_labels.append([player_answer[item], row_formats[count]])
            all_labels.append([correct_god[item], row_formats[count]])
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
        quest_1 = str(stats_list)
        quest_2 = str(stats_list)
        quest_3 = str(stats_list)
        quest_4 = str(stats_list)

        return [entity, quest_1, quest_2, quest_3, quest_4]

    def close_stats(self, partner):
        partner.to_stats_btn.config(state="normal")
        self.stats_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    ChooseRounds()
    root.mainloop()
