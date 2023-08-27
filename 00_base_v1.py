from tkinter import *
from functools import partial  # To import unwanted windows


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

        to_questions = self.check_rounds(1, 50)

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

        self.quiz_frame = Frame(self.quiz_box, padx=10, pady=10)
        self.quiz_frame.grid()

        rounds_heading = "Name? - Question 1 of {}".format(rounds_choice)
        self.naming_heading = Label(self.quiz_frame, text=rounds_heading,
                                    font=("Georgia", "16", "bold")
                                    )
        self.naming_heading.grid(row=0)

    def close_quiz(self):
        root.deiconify()
        self.quiz_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Greek/Roman Gods Quiz")
    Start()
    root.mainloop()
