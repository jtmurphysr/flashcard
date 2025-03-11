import sqlite3
import csv
import os
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


def import_from_csv(conn, csv_file_path):
    """
    Import flashcards from a CSV file.

    Parameters:
    conn (sqlite3.Connection): Database connection
    csv_file_path (str): Path to the CSV file

    Returns:
    int: Number of records imported
    """
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        return 0

    cursor = conn.cursor()
    counter = 0

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Skip header row if it exists
            header = next(csv_reader, None)
            if header and "target_word" in header[0].lower():
                pass  # Skip the header
            else:
                # If no header, rewind to start of file
                csv_file.seek(0)

            for row in csv_reader:
                if len(row) >= 2:  # Ensure we have at least target and native words
                    target_word = row[0].strip()
                    native_word = row[1].strip()

                    # Check if the card already exists
                    cursor.execute(
                        "SELECT id FROM flashcards WHERE target_word = ? AND native_word = ?",
                        (target_word, native_word)
                    )
                    existing = cursor.fetchone()

                    if not existing:
                        cursor.execute('''
                        INSERT INTO flashcards (target_word, native_word, last_displayed, last_correct, correct_count)
                        VALUES (?, ?, NULL, NULL, 0)
                        ''', (target_word, native_word))
                        counter += 1

        conn.commit()
        return counter
    except Exception as e:
        print(f"Error importing from CSV: {e}")
        return 0


def get_all_csv_files(directory):
    """
    Get all CSV files in the specified directory.

    Parameters:
    directory (str): Directory path to search

    Returns:
    list: List of paths to CSV files
    """
    csv_files = []
    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            if filename.lower().endswith('.csv'):
                csv_files.append(os.path.join(directory, filename))
    return csv_files


def get_cards_for_review(conn, days_multiplier=7):
    """
    Get flashcards that are due for review based on their correct_count and last_correct date.
    
    Parameters:
    conn (sqlite3.Connection): Database connection
    days_multiplier (int): Number of days to wait per correct answer
    
    Returns:
    list: List of dictionaries containing card information
    """
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, target_word, native_word, last_displayed, last_correct, correct_count
    FROM flashcards
    WHERE last_correct IS NULL
       OR datetime(last_correct, '+' || (correct_count * ?) || ' days') <= datetime('now')
    ''', (days_multiplier,))
    
    cards = []
    for row in cursor.fetchall():
        cards.append({
            'id': row[0],
            'target_word': row[1],
            'native_word': row[2],
            'last_displayed': row[3],
            'last_correct': row[4],
            'correct_count': row[5]
        })
    return cards


def update_card_status(conn, card_id, correct=True):
    """Update a card's status after review."""
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    print(f"Updating card {card_id}, correct={correct}")  # Debug print
    
    if correct:
        sql = '''
        UPDATE flashcards
        SET last_displayed = ?,
            last_correct = ?,
            correct_count = correct_count + 1
        WHERE id = ?
        '''
        params = (now, now, card_id)
    else:
        sql = '''
        UPDATE flashcards
        SET last_displayed = ?,
            correct_count = CASE 
                WHEN correct_count > 0 THEN correct_count - 1
                ELSE 0
            END
        WHERE id = ?
        '''
        params = (now, card_id)
    
    print(f"Executing SQL: {sql}")  # Debug print
    print(f"With parameters: {params}")  # Debug print
    
    cursor.execute(sql, params)
    rows_affected = cursor.rowcount
    print(f"Rows affected by update: {rows_affected}")  # Debug print
    
    conn.commit()
    print("Changes committed to database")  # Debug print
    
    # Verify the update
    cursor.execute('SELECT * FROM flashcards WHERE id = ?', (card_id,))
    result = cursor.fetchone()
    print(f"Card state after update: {result}")  # Debug print


def main():
    # Create the database and tables
    conn = create_flashcards_db()

    # Add sample data
    add_sample_flashcards(conn)

    # Import from CSV files in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    csv_files = get_all_csv_files(data_dir)

    total_imported = 0
    if csv_files:
        print(f"Found {len(csv_files)} CSV files in the data directory:")
        for csv_file in csv_files:
            print(f"  - {os.path.basename(csv_file)}")
            imported = import_from_csv(conn, csv_file)
            total_imported += imported
            print(f"    Imported {imported} new flashcards")
    else:
        print("No CSV files found in the data directory.")

    # Query to verify data
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flashcards')
    rows = cursor.fetchall()

    print(f"\nDatabase Summary:")
    print(f"{'ID':<3} {'Target Word':<15} {'Native Word':<15} {'Correct Count':<15}")
    print("-" * 50)
    for row in rows:
        print(f"{row[0]:<3} {row[1]:<15} {row[2]:<15} {row[5]:<15}")

    # Close the connection
    conn.close()
    print(f"\nDatabase created successfully with {total_imported} flashcards imported from CSV!")


if __name__ == "__main__":
    main()