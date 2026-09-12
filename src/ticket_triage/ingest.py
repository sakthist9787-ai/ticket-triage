"""Ingestion utilities: load tickets from CSV or JSON files."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path

from .exceptions import (
    EmptyDatasetError,
    InvalidTicketDataError,
    UnsupportedFileFormatError,
)
from .models import Ticket

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".csv", ".json"}


def load_tickets(path: str | Path, strict: bool = False) -> list[Ticket]:
    """Load tickets from a CSV or JSON file.

    Args:
        path: path to a .csv or .json file.
        strict: if True, raise on the first malformed record. If False (default),
            skip malformed records and log a warning for each.

    Returns:
        A list of validated Ticket objects.

    Raises:
        FileNotFoundError: if the path does not exist.
        UnsupportedFileFormatError: if the file extension isn't .csv or .json.
        EmptyDatasetError: if no valid tickets could be parsed.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileFormatError(
            f"Unsupported input format '{suffix}'. Supported: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    raw_records = _read_csv(path) if suffix == ".csv" else _read_json(path)

    tickets: list[Ticket] = []
    for i, raw in enumerate(raw_records):
        try:
            tickets.append(Ticket.from_dict(raw))
        except InvalidTicketDataError as exc:
            if strict:
                raise
            logger.warning("Skipping malformed record at index %d: %s", i, exc)

    if not tickets:
        raise EmptyDatasetError(f"No valid tickets could be parsed from {path}")

    logger.info("Loaded %d valid ticket(s) from %s", len(tickets), path)
    return tickets


def _read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _read_json(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        # allow either a top-level list-wrapping key or a single record
        if "tickets" in data:
            data = data["tickets"]
        else:
            data = [data]

    if not isinstance(data, list):
        raise InvalidTicketDataError("JSON input must be a list of ticket records")

    return data
