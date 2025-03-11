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
   pip install pandas tkinter sqlite3
   ```

3. Run the launcher application:
   ```
   python flashcard_launcher.py
   ```

## Database Structure

The application uses SQLite to store flashcards and track progress:

- **flashcards table**:
  - `id`: Unique identifier for each card
  - `target_word`: Word in the language being learned
  - `native_word`: Translation in native language
  - `last_displayed`: Timestamp of last review
  - `last_correct`: Timestamp of last correct answer
  - `correct_count`: Number of times answered correctly
  - `created_at`: Card creation timestamp

## Spaced Repetition System

The application implements a simple spaced repetition system:
- Cards are shown more frequently when new or answered incorrectly
- Each correct answer increases the interval before the card appears again
- Interval = correct_count * 7 days
- Incorrect answers decrease the correct_count

## CSV File Structure

To create your own flashcard sets, you'll need to prepare a CSV file with the appropriate structure. The CSV file must have at least two columns, with headers that match the "front_lang" and "back_lang" values you specify in the launcher.

### Example CSV Structures

#### Language Learning (e.g., Italian_500.csv)
```csv
Italian,English
ciao,hello
grazie,thank you
buongiorno,good morning
gatto,cat
```

#### Chemistry Elements (e.g., chemistry_elements.csv)
```csv
Element,Symbol,AtomicNumber
Hydrogen,H,1
Helium,He,2
Lithium,Li,3
Beryllium,Be,4
```
*Note: When using this set, set front_lang="Element" and back_lang="Symbol"*

#### Mathematical Formulas (e.g., math_formulas.csv)
```csv
Formula,Description
a² + b² = c²,Pythagorean theorem
E = mc²,Einstein's mass-energy equivalence
F = ma,Newton's second law
```

## Using the Application

### Launcher

The launcher is the main entry point for the application. It allows you to:
- Select a flashcard set to study
- Add new flashcard sets
- Edit existing sets
- View statistics for each set

### Studying Flashcards

When studying flashcards:
1. The front of the card is shown first
2. After 5 seconds, the card flips automatically to show the answer
3. You can mark cards as "Known" using the checkmark button
4. Cards marked as "Known" are saved to a separate file and removed from the current rotation
5. You can review unknown cards by clicking the X button

### Adding Custom Sets

To add a new flashcard set:
1. Click "Add New Set" in the launcher
2. Enter a name for your set (e.g., "Spanish Vocabulary")
3. Browse to select your CSV file
4. Specify the column names for the front and back of cards
5. Click "Save"

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
