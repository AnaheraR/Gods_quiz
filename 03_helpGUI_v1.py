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

        self.quiz_frame = Frame(self.quiz_box, padx=10, pady=10)
        self.quiz_frame.grid()

        self.control_frame = Frame(self.quiz_frame)
        self.control_frame.grid(row=5)

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

        # disable stats button
        self.to_help_btn = self.control_button_ref[0]
        self.to_stats_btn = self.control_button_ref[1]
        self.to_stats_btn.config(state=DISABLED)

    def to_do(self, action):
        if action == "get help":
            DisplayHelp(self)
        elif action == "get stats:":
            pass
        else:
            self.close_play()

    # DON'T USE THIS FUNCTION IN BASE AS IT KILLS THE ROOT
    def close_play(self):
        root.destroy()


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


if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    ChooseRounds()
    root.mainloop()
