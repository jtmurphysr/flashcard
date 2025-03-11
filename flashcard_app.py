from tkinter import Tk, Canvas, PhotoImage, Button
import pandas as pd
import random
import sqlite3


class FlashcardApp:
    """A flashcard application for language learning."""
    
    # Class constants
    BACKGROUND_COLOR = "#B1DDC6"
    FLIP_DELAY = 5000  # Time before card flips (ms)
    NEXT_CARD_DELAY = 3000  # Time before next card appears after flip (ms)
    
    def __init__(self, db_path='flashcards.db', front_lang="Target", back_lang="Native", days_multiplier=7):
        """Initialize the flashcard application.
        
        Args:
            db_path (str): Path to the SQLite database
            front_lang (str): Label for the front of the cards
            back_lang (str): Label for the back of the cards
            days_multiplier (int): Number of days to multiply by correct_count for spacing
        """
        print(f"Connecting to database: {db_path}")
        self.conn = sqlite3.connect(db_path)
        
        # Test the connection
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM flashcards')
        count = cursor.fetchone()[0]
        print(f"Found {count} cards in database")
        
        self.days_multiplier = days_multiplier
        self.current_cards = []
        self.current_card = None
        self.front_lang = front_lang
        self.back_lang = back_lang
        self.flip_timer = None
        self.next_card_timer = None
        
        # Set up the UI
        self._setup_ui()
        
        # Load cards and display the first one
        self._load_cards()
        self.next_card()
    
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
            command=self.mark_unknown,
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
    
    def _load_cards(self):
        """Load cards that are due for review."""
        from load_db import get_cards_for_review
        self.current_cards = get_cards_for_review(self.conn, self.days_multiplier)
        print(f"Loaded {len(self.current_cards)} cards for review")  # Debug print
        for card in self.current_cards[:3]:  # Print first 3 cards as sample
            print(f"Card: {card}")
        random.shuffle(self.current_cards)
    
    def next_card(self):
        """Display the next flashcard."""
        if not self.current_cards:
            self._load_cards()
            if not self.current_cards:
                self.show_completion_message()
                return

        self._cancel_timers()
        self.current_card = self.current_cards.pop()
        
        # Update display
        self.canvas.itemconfig(self.card_background, image=self.card_front_img)
        self.canvas.itemconfig(self.card_title, text=self.front_lang, fill="black")
        self.canvas.itemconfig(self.card_word, text=self.current_card['target_word'], fill="black")
        
        # Set flip timer
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
        self.canvas.itemconfig(self.card_word, text=self.current_card['native_word'], fill="white")
        
        # Set a timer to show the next card automatically
        self.next_card_timer = self.window.after(self.NEXT_CARD_DELAY, self.next_card)
    
    def mark_known(self):
        """Mark the current card as known."""
        if not self.current_card:
            print("No current card to mark as known!")  # Debug print
            return

        print(f"Current card before update: {self.current_card}")  # Debug print
        
        cursor = self.conn.cursor()
        # Check current status
        cursor.execute('SELECT * FROM flashcards WHERE id = ?', (self.current_card['id'],))
        before = cursor.fetchone()
        print(f"Database state before update: {before}")  # Debug print

        from load_db import update_card_status
        update_card_status(self.conn, self.current_card['id'], correct=True)
        
        # Verify the update
        cursor.execute('SELECT * FROM flashcards WHERE id = ?', (self.current_card['id'],))
        after = cursor.fetchone()
        print(f"Database state after update: {after}")  # Debug print
        
        self.next_card()
    
    def mark_unknown(self):
        """Mark the current card as unknown."""
        if not self.current_card:
            return

        from load_db import update_card_status
        update_card_status(self.conn, self.current_card['id'], correct=False)
        self.next_card()
    
    def show_completion_message(self):
        """Show a message when all cards are completed."""
        self.canvas.itemconfig(self.card_title, text="Great job!", fill="black")
        self.canvas.itemconfig(self.card_word, text="No more cards to review\nfor now!", fill="black")
    
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
