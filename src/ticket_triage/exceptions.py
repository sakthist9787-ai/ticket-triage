"""Custom exceptions for the ticket triage tool."""


class TicketTriageError(Exception):
    """Base exception for all ticket triage errors."""


class InvalidTicketDataError(TicketTriageError):
    """Raised when ticket data is missing required fields or malformed."""


class UnsupportedFileFormatError(TicketTriageError):
    """Raised when an input/output file format is not supported."""


class EmptyDatasetError(TicketTriageError):
    """Raised when a dataset contains no valid tickets to process."""
