# Flashy - Italian-English Flashcard App

Flashy is a simple flashcard application built with Python and Tkinter. The app displays Italian words on flashcards and allows users to practice learning their English translations. It provides an interactive interface to help users review vocabulary and mark words as "known" or "unknown."

---

## Features

- Displays random Italian words on flashcards.
- Flips the card after 5 seconds to show the English translation.
- Two buttons (`✔️ Known` or `❌ Unknown`) to mark your response.
- Tracks progress by removing "known" words from the word list.
- Designed with an intuitive and minimalistic user interface.

---

## Requirements

Make sure you have the following libraries installed:

- **Python 3.13.0 or higher**
- Required Python libraries:
  - **pandas** - For importing and manipulating word data.
  - **tkinter** - For building the graphical user interface.

To install any missing libraries, run:

```bash
pip install pandas
```

---

## Installation

1. Clone or download this repository to your local machine.
2. Make sure the following folder structure exists:
   ```
   .
   ├── data/
   │   └── Italian_500.csv
   ├── images/
   │   ├── card_front.png
   │   ├── card_back.png
   │   ├── wrong.png
   │   └── right.png
   ├── main.py
   ```
   
   - **data/Italian_500.csv**: A CSV file containing the word list. The file should include two columns: `Italian` and `English` for word pairs.
   - **images/**: Contains the image assets for the flashcards and buttons.
   
3. Run the main program:

   ```bash
   python main.py
   ```

---

## How to Use

1. **Start the app:** The first flashcard will be displayed with an Italian word.
2. **Study the Italian word** and its translation:
   - The card will flip automatically after 5 seconds to reveal the English translation.
3. **Mark your response:**
   - Click on `❌` if you don't know the word (this will show a new card).
   - Click on `✔️` if you know the word (this removes it from the word list).
4. **Repeat the process** until you master all the words!

---

## Folder and File Structure

- **data/Italian_500.csv**: A CSV file containing Italian-English word pairs in the following format:
  ```
  Italian,English
  casa,house
  libro,book
  ...
  ```
- **images/**: Contains all the image assets used in the app.
  - `card_front.png`: Image for the front side of the flashcard.
  - `card_back.png`: Image for the back side of the flashcard.
  - `wrong.png`: Image for the `❌` button.
  - `right.png`: Image for the `✔️` button.
- **main.py**: The main script to run the application.

---

## Code Overview

### Key Functions

- `pick_word()`:
  Picks a random word from the vocabulary dataset.

- `next_card()`:
  Displays the next flashcard and sets a timer to flip it after 5 seconds.

- `flip_card()`:
  Flips the current flashcard to show the English translation.

- `is_known()`:
  Removes the current word from the dataset and displays the next card.

---

## Example Output

### Flashcard UI
- Front side of the card will show:
  
  **Italian Word**  
  _E.g., "libro"_

- After 5 seconds, the card flips to show:

  **English Word**  
  _E.g., "book"_

### User Interaction
- Clicking `✔️`: Removes the word from the learning set.
- Clicking `❌`: Skips to a new flashcard.

---

## Known Issues or Limitations

- The app does not currently save progress between sessions. If you close the app, it will start over with all the words in the dataset.
- Words are deleted only for the current session; no modifications are saved to the `Italian_500.csv` file.

---

## Future Enhancements

Here are some ideas for future improvements:

1. **Progress Tracking**: Save and load progress across sessions.
2. **Dynamic Dataset**: Allow users to add their own word sets.
3. **Statistics**: Track and display learning progress.
4. **Enhanced UI**: Add animations or better visual feedback.

---

## Contributing

If you want to contribute to this project:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-feature`.
3. Commit your changes: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.