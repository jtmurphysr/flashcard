from random import random
from tkinter import Tk, Canvas, PhotoImage, Button, Label
import pandas
import random

# Global variables to store the current card text and the index of the selected word
global card_text
global word_index
word_dict = {}
card_text = {}

# Try to read the Italian-English word data from a CSV file
# If the file does not exist, print an error message and exit the program
try:
    data = pandas.read_csv("data/Italian_500 .csv")
    word_dict = data.to_dict(orient="records")  # Convert the CSV data to a list of dictionaries
except FileNotFoundError:
    print("File not found")
    exit()


# Function to pick a random word from the word dictionary
def pick_word():
    global word_index
    # Generate a random index within the bounds of the word dictionary
    word_index = random.randint(0, len(word_dict) - 1)
    picked_word = word_dict[word_index]  # Select the word at the generated index
    print(picked_word)  # Print the selected word (for debugging purposes)
    return picked_word


# Constant for the background color of the application
BACKGROUND_COLOR = "#B1DDC6"


# Function to display the next flashcard with the Italian word on the front
def next_card():
    global card_text
    # Get a randomly selected word from the word dictionary
    card_text = pick_word()
    print(type(card_text))  # Print the card text data type (for debugging purposes)
    front_word = card_text["Italian"]  # Extract the Italian word from the selected word
    # Update the canvas to display the Italian word
    canvas.itemconfig(card_title, text="Italian", fill="black")
    canvas.itemconfig(card_word, text=front_word, fill="black")
    back_word = card_text["English"]  # Extract the English word (for reverse translation)
    print(front_word, back_word)  # Print both words (for debugging purposes)
    # Set a timer to flip the card and show the English word after 5 seconds
    flip_timer = window.after(5000, func=flip_card)


# Function to flip the card and show the English translation on the back
def flip_card():
    back_word = card_text["English"]  # Get the English translation of the current word
    # Update the canvas to display the English word
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=back_word, fill="black")


# Function to handle the "Known" action, removing the current word from the dictionary
def is_known():
    # Print the currently known word (for debugging purposes)
    print(word_dict[word_index])
    del word_dict[word_index]  # Remove the known word from the word dictionary
    next_card()  # Display the next flashcard


# ---------------------------- UI SETUP ------------------------------- #
# Initialize the main Tkinter window
window = Tk()
window.title("Flashy")  # Set the title of the application
# Configure the window with padding and a background color
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Create a canvas to display the flashcard images and text
canvas = Canvas(width=800, height=526)
# Load the card front and back images
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
# Set the background of the canvas with the flashcard front image
card_background = canvas.create_image(400, 263, image=card_front_img)
# Create text placeholders for the card title and words
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
# Configure the canvas background and remove highlight borders
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
# Place the canvas in the grid layout
canvas.grid(row=0, column=0, columnspan=2)

# Create a button for the "Unknown" action (incorrect response)
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)  # Add the button to the grid layout

# Create a button for the "Known" action (correct response)
check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)  # Add the button to the grid layout

# Display the first flashcard when the program starts
next_card()

# Start the Tkinter main event loop to run the application
window.mainloop()