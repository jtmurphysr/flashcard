import sqlite3
from datetime import datetime


def create_flashcards_db(db_path='flashcards.db'):
    """
    Create a SQLite database for a flashcard application.

    Parameters:
    db_path (str): Path to the database file

    Returns:
    sqlite3.Connection: Database connection object
    """
    # Connect to database (will create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the flashcards table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target_word TEXT NOT NULL,          -- Word in the language being learned
        native_word TEXT NOT NULL,          -- Translation in native language
        last_displayed TIMESTAMP,           -- Last time the card was shown
        last_correct TIMESTAMP,             -- Last time user answered correctly
        correct_count INTEGER DEFAULT 0,    -- Number of times answered correctly
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_target ON flashcards(target_word)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_last_displayed ON flashcards(last_displayed)')

    # Commit changes and return connection
    conn.commit()
    return conn


def add_sample_flashcards(conn):
    """
    Add a few sample flashcards to the database.

    Parameters:
    conn (sqlite3.Connection): Database connection
    """
    sample_cards = [
        ('hola', 'hello', None, None, 0),
        ('gracias', 'thank you', None, None, 0),
        ('por favor', 'please', None, None, 0),
        ('adiós', 'goodbye', None, None, 0)
    ]

    cursor = conn.cursor()
    cursor.executemany('''
    INSERT INTO flashcards (target_word, native_word, last_displayed, last_correct, correct_count)
    VALUES (?, ?, ?, ?, ?)
    ''', sample_cards)

    conn.commit()


def main():
    # Create the database and tables
    conn = create_flashcards_db()

    # Add sample data
    add_sample_flashcards(conn)

    # Query to verify data
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flashcards')
    rows = cursor.fetchall()

    print(f"{'ID':<3} {'Target Word':<15} {'Native Word':<15} {'Correct Count':<15}")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:<3} {row[1]:<15} {row[2]:<15} {row[5]:<15}")

    # Close the connection
    conn.close()
    print("\nDatabase created successfully!")


if __name__ == "__main__":
    main()