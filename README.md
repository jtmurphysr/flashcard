# Flashcard Learning System

A versatile flashcard application for learning languages, memorizing facts, studying concepts, or mastering any subject that benefits from spaced repetition learning.

## Features

- **Flexible Learning**: Study any subject with customizable flashcard sets
- **Progress Tracking**: Automatically saves your progress for each study set
- **Multiple Sets**: Maintain different flashcard collections for various subjects
- **User-Friendly Interface**: Clean, intuitive design with minimal distractions
- **Spaced Repetition**: Cards appear less frequently as you learn them (7-day multiplier per correct answer)
- **Customizable**: Add your own sets by creating simple CSV files
- **Persistent Storage**: SQLite database maintains progress across sessions
- **Error Handling**: Robust error recovery and user-friendly error messages

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/flashcard-system.git
   cd flashcard-system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the launcher application:
   ```
   python flashcard_launcher.py
   ```

## Database Structure

The application uses SQLite to store flashcards and track progress. All flashcard data is stored in a local database file (flashcards.db):

- **flashcards table**:
  - `id`: Unique identifier for each card
  - `target_word`: Word in the language being learned
  - `native_word`: Translation in native language
  - `last_displayed`: Timestamp of last review
  - `last_correct`: Timestamp of last correct answer
  - `correct_count`: Number of times answered correctly
  - `created_at`: Card creation timestamp

## Spaced Repetition System

The application implements a smart spaced repetition system:
- New cards and incorrectly answered cards are shown more frequently
- Each correct answer increases the interval before the card appears again
- Interval = correct_count * 7 days
- Incorrect answers decrease the correct_count by 1 (minimum 0)
- Cards are automatically scheduled based on your performance

## Adding New Flashcards

### Using the Launcher

1. Click "Add New Set" in the launcher
2. Enter a name for your set (e.g., "Spanish Vocabulary")
3. Either:
   - Browse to select a CSV file for import
   - Or manually add cards through the interface
4. Specify the languages/categories for the front and back of cards
5. Click "Save"

### Importing from CSV

You can import flashcards from CSV files. The CSV should have two columns:

```csv
target_word,native_word
ciao,hello
grazie,thank you
```

The application will:
1. Create new database entries for each word pair
2. Initialize tracking data (correct_count, timestamps, etc.)
3. Begin scheduling the cards based on the spaced repetition system

## Using the Application

### Launcher

The launcher provides:
- Flashcard set management
- Progress statistics for each set
- Import/export functionality
- Set configuration

### Studying Flashcards

When studying:
1. Cards are presented based on their review schedule
2. The front of the card is shown for 5 seconds
3. The card automatically flips to show the answer
4. Mark your response:
   - ✓ (Correct): Increases interval and correct_count
   - ✗ (Incorrect): Decreases interval and correct_count

## Project Structure

- `flashcard_launcher.py`: The main launcher application
- `flashcard_app.py`: The core flashcard functionality
- `flashcard_sets.json`: Configuration file storing sets information
- `data/`: Directory containing CSV files for different flashcard sets
- `images/`: Contains UI images like card templates and buttons

## Customization

### Changing Card Appearance

The application uses image files for card fronts and backs. You can replace these images with your own designs:
- `images/card_front.png`: Image for the front of the card
- `images/card_back.png`: Image for the back of the card

### Adjusting Timings

You can modify the time before cards flip and other timing settings by changing the constants in the `FlashcardApp` class.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to all contributors who have helped improve this application
- Inspired by spaced repetition learning systems
