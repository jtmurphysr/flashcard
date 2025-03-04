from tkinter import Tk, Canvas, PhotoImage, Button
import pandas as pd
import random


class FlashcardApp:
    """A flashcard application for language learning."""
    
    # Class constants
    BACKGROUND_COLOR = "#B1DDC6"
    FLIP_DELAY = 5000  # Time before card flips (ms)
    NEXT_CARD_DELAY = 3000  # Time before next card appears after flip (ms)
    
    def __init__(self, data_file="data/Italian_500 .csv", front_lang="Italian", back_lang="English"):
        """Initialize the flashcard application.
        
        Args:
            data_file (str): Path to the CSV file containing word pairs
            front_lang (str): The language to display on the front of cards
            back_lang (str): The language to display on the back of cards
        """
        self.data_file = data_file
        self.front_lang = front_lang
        self.back_lang = back_lang
        self.words = self._load_words(data_file)
        self.current_card = None
        self.flip_timer = None
        self.next_card_timer = None
        
        # Set up the UI
        self._setup_ui()
        
        # Display the first card
        self.next_card()
    
    def _load_words(self, data_file):
        """Load word pairs from a CSV file.
        
        Args:
            data_file (str): Path to the CSV file containing word pairs
            
        Returns:
            list: A list of dictionaries with word pairs
            
        Raises:
            SystemExit: If the file is not found
        """
        try:
            data = pd.read_csv(data_file)
            return data.to_dict(orient="records")
        except FileNotFoundError:
            print(f"Error: File '{data_file}' not found")
            exit(1)
    
    def _setup_ui(self):
        """Set up the user interface."""
        # Initialize the main window
        self.window = Tk()
        self.window.title("Flashy")
        self.window.config(padx=50, pady=50, bg=self.BACKGROUND_COLOR)
        
        # Create the canvas for displaying cards
        self.canvas = Canvas(width=800, height=526)
        self.canvas.config(bg=self.BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)
        
        # Load card images
        self.card_front_img = PhotoImage(file="images/card_front.png")
        self.card_back_img = PhotoImage(file="images/card_back.png")
        
        # Create card elements
        self.card_background = self.canvas.create_image(400, 263, image=self.card_front_img)
        self.card_title = self.canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
        self.card_word = self.canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
        
        # Create buttons
        cross_image = PhotoImage(file="images/wrong.png")
        unknown_button = Button(
            image=cross_image, 
            highlightthickness=0, 
            command=self.flip_card,
            bg=self.BACKGROUND_COLOR
        )
        unknown_button.grid(row=1, column=0)
        
        check_image = PhotoImage(file="images/right.png")
        known_button = Button(
            image=check_image, 
            highlightthickness=0, 
            command=self.mark_known,
            bg=self.BACKGROUND_COLOR
        )
        known_button.grid(row=1, column=1)
        
        # Save references to prevent garbage collection
        unknown_button.image = cross_image
        known_button.image = check_image
    
    def pick_word(self):
        """Select a random word from the available words.
        
        Returns:
            dict: A dictionary containing the word pair
        """
        if not self.words:
            # If all words are known, show a congratulatory message
            self._show_completion_message()
            return None
            
        return random.choice(self.words)
    
    def _show_completion_message(self):
        """Show a message when all words have been learned."""
        self.canvas.itemconfig(self.card_title, text="Congratulations!", fill="black")
        self.canvas.itemconfig(self.card_word, text="You've learned all words!", fill="black")
    
    def next_card(self):
        """Display the next flashcard."""
        # Cancel any existing timers
        self._cancel_timers()
        
        # Get a new word
        self.current_card = self.pick_word()
        if not self.current_card:
            return
            
        # Update the UI to show the front of the card
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.canvas.itemconfig(self.card_title, text=self.front_lang, fill="black")
        self.canvas.itemconfig(self.card_word, text=self.current_card[self.front_lang], fill="black")
        
        # Set a timer to flip the card automatically
        self.flip_timer = self.window.after(self.FLIP_DELAY, self.flip_card)
    
    def flip_card(self):
        """Flip the card to show the translation."""
        # Cancel the flip timer if it exists
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)
            self.flip_timer = None
            
        if not self.current_card:
            return
            
        # Update the UI to show the back of the card
        self.canvas.itemconfig(self.card_background, image=self.card_back_img)
        self.canvas.itemconfig(self.card_title, text=self.back_lang, fill="white")
        self.canvas.itemconfig(self.card_word, text=self.current_card[self.back_lang], fill="white")
        
        # Set a timer to show the next card automatically
        self.next_card_timer = self.window.after(self.NEXT_CARD_DELAY, self.next_card)
    
    def mark_known(self):
        """Mark the current word as known, save to known_words.json, and proceed to the next word."""
        if not self.current_card:
            return
            
        # Define the known words file path
        import os
        import json
        from tkinter import messagebox
        
        # Get the directory of the data file
        data_dir = os.path.dirname(os.path.abspath(self.data_file))
        # Create a filename based on the original data file name
        base_name = os.path.splitext(os.path.basename(self.data_file))[0]
        known_file = os.path.join(data_dir, f"{base_name}_known_words.json")
        
        try:
            # Load existing known words
            try:
                with open(known_file, "r") as data_file:
                    known_words = json.load(data_file)
            except FileNotFoundError:
                # If the file does not exist, start with an empty list
                known_words = []
                
            # Add the current card to known words
            known_words.append(self.current_card)
            
            # Save updated known words back to the file
            with open(known_file, "w") as data_file:
                json.dump(known_words, data_file, indent=4)
                
            # Remove the word from the current deck
            if self.current_card in self.words:
                self.words.remove(self.current_card)
                
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Could not save known word: {str(e)}")
            
        # Move to next card
        self.next_card()
    
    def _cancel_timers(self):
        """Cancel any active timers to prevent memory leaks."""
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)
            self.flip_timer = None
            
        if self.next_card_timer:
            self.window.after_cancel(self.next_card_timer)
            self.next_card_timer = None
    
    def run(self):
        """Start the application's main loop."""
        self.window.mainloop()


if __name__ == "__main__":
    app = FlashcardApp()
    app.run()
