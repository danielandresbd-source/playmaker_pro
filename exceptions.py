# exceptions.py
# Custom exceptions for PlayMaker Pro
# I learned about custom exceptions in class and they make error handling
# way cleaner than just throwing generic Exceptions everywhere


class PlayMakerError(Exception):
    """Base exception for all errors in this app.

    Every custom exception inherits from this so you can catch
    all our errors with just 'except PlayMakerError'.
    """
    pass


class ValidationError(PlayMakerError):
    """Raised when data doesn't pass our validation checks.

    For example: yards = -99, empty play name, invalid formation, etc.
    """
    pass


class PlaybookNotFoundError(PlayMakerError):
    """Raised when we try to find a playbook by ID and it doesn't exist.

    Args:
        playbook_id: the ID we searched for
    """
    def __init__(self, playbook_id):
        self.playbook_id = playbook_id
        super().__init__(f"Playbook with ID '{playbook_id}' not found.")


class PlayNotFoundError(PlayMakerError):
    """Raised when we can't find a specific play.

    Args:
        play_id: the ID we searched for
    """
    def __init__(self, play_id):
        self.play_id = play_id
        super().__init__(f"Play with ID '{play_id}' not found.")


class DataImportError(PlayMakerError):
    """Raised when something goes wrong while importing CSV data.

    Could be a missing file, wrong format, missing columns, etc.
    """
    pass


class StorageError(PlayMakerError):
    """Raised when we can't read or write the JSON storage file.

    This usually means the file is corrupted or we don't have permissions.
    """
    pass
