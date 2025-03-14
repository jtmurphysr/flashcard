from random import random
from tkinter import Tk, Canvas, PhotoImage, Button, Label
import pandas
import random


global card_text
global word_index
global card_title
global card_word

word_dict = {}
card_text = {}

try:
    data = pandas.read_csv("data/Italian_500 .csv")
    word_dict = data.to_dict(orient="records")
except FileNotFoundError:
    print("Error: Could not find 'data/Italian_500 .csv'. Please ensure the file exists in the data directory.")
    exit(1)  # Use exit code 1 to indicate error

def pick_word():
    global word_index
    word_index = random.randint(0, len(word_dict) - 1)
    picked_word = word_dict[word_index]
    print(picked_word)
    return picked_word

BACKGROUND_COLOR = "#B1DDC6"

def next_card():
    global card_text, flip_timer
    if 'flip_timer' in globals():
        window.after_cancel(flip_timer)
    card_text = pick_word()
    print(type(card_text))
    front_word = card_text["Italian"]
    canvas.itemconfig(card_title, text="Italian", fill="black")
    canvas.itemconfig(card_word, text=front_word, fill="black")
    back_word = card_text["English"]
    print(front_word, back_word)
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    back_word = card_text["English"]
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=back_word, fill="black")

def is_known():
    global word_dict
    del word_dict[word_index]
    if not word_dict:
        canvas.itemconfig(card_word, text="No more words!")
        return
    next_card()
    del word_dict[word_index]
    next_card()

    #delete picked_word from word_dict




def main():
    # ---------------------------- UI SETUP ------------------------------- #
    global canvas, window, card_title, card_word
    
    window = Tk()  # Create window here instead
    window.title("Flashy")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    canvas = Canvas(width=800, height=526)  # Create canvas here instead
    canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=2)

    card_front_img = PhotoImage(file="images/card_front.png")
    card_back_img = PhotoImage(file="images/card_back.png")
    card_background = canvas.create_image(400, 263, image=card_front_img)
    card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
    card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

    cross_image = PhotoImage(file="images/wrong.png")
    unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
    unknown_button.grid(row=1, column=0)

    check_image = PhotoImage(file="images/right.png")
    known_button = Button(image=check_image, highlightthickness=0, command=is_known)
    known_button.grid(row=1, column=1)

    next_card()

    window.mainloop()

if __name__ == "__main__":
    main()