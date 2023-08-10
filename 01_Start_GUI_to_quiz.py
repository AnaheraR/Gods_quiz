from tkinter import *
from functools import partial  # To import unwanted windows


class ChooseRounds:

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
                                  "of rounds you'd like to play...\n"
        self.choose_instructions_label = Label(self.start_frame,
                                               text=choose_instructions_txt,
                                               wraplength=380, justify="center")
        self.choose_instructions_label.grid(row=1)

        self.rounds_choice_frame = Frame(self.start_frame)
        self.rounds_choice_frame.grid(row=2)

        self.round_entry = Entry(self.rounds_choice_frame,
                                 font=("Georgia", "14")
                                 )
        self.round_entry.grid(row=0, column=0, padx=10, pady=10)

        self.output_label = Label(self.rounds_choice_frame,
                                  text="", fg="#9C0000")
        self.output_label.grid(row=3)

        self.enter_button = Button(self.rounds_choice_frame, text="Enter",
                                   bg="#FFE6CC", fg=button_fg, font=button_font,
                                   width=12, command=self.to_quiz)
        self.enter_button.grid(row=0, column=1, padx=10, pady=10)

    def to_quiz(self, num_rounds):
        Quiz(num_rounds)

        # Hide root window
        root.withdraw()


class Quiz:

    def __init__(self, how_many):
        self.quiz_box = Toplevel()
        # if users press cross at top, closes
        # the box
        self.quiz_box.protocol('WM_DELETE_WINDOW',
                               partial(self.close_quiz))

        self.quiz_frame = Frame(self.quiz_box, padx=10, pady=10)
        self.quiz_frame.grid()

        rounds_heading = "Name? - Round 1 of {}".format(how_many)
        self.naming_heading = Label(self.quiz_frame, text=rounds_heading,
                                    font=("Georgia", "16", "bold")
                                    )
        self.naming_heading.grid(row=0)

    def close_quiz(self):
        root.deiconify()



if __name__ == "__main__":
    root = Tk()
    root.title("Greek/Roman Gods Quiz")
    ChooseRounds()
    root.mainloop()
