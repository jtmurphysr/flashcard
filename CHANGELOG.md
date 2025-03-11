# Changelog

## [1.1.0] - 2024-03-XX

### Added
- SQLite database integration for persistent storage
- Spaced repetition system with 7-day multiplier
- Progress tracking for each flashcard
- Comprehensive error handling system
- User-friendly error messages
- Database connection management
- Automatic database creation if not exists

### Changed
- Moved from CSV-based storage to SQLite database
- Updated card loading mechanism to use spaced repetition
- Improved progress tracking with correct_count
- Enhanced error reporting and recovery

### Fixed
- Memory leaks from timer management
- Database connection handling
- Error handling for missing files

## [1.0.0] - Initial Release

### Features
- Basic flashcard functionality
- CSV file support
- Simple user interface
- Basic progress tracking
- Multiple language support
- Customizable flashcard sets 