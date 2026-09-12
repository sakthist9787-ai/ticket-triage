"""Export triaged tickets to CSV or JSON."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path

from .exceptions import UnsupportedFileFormatError
from .models import Ticket

logger = logging.getLogger(__name__)

FIELDNAMES = [
    "ticket_id", "subject", "body", "customer", "created_at",
    "category", "urgency", "matched_keywords",
]


def export_tickets(tickets: list[Ticket], path: str | Path) -> None:
    """Write triaged tickets to a CSV or JSON file, inferred from the extension."""
    path = Path(path)
    suffix = path.suffix.lower()
    path.parent.mkdir(parents=True, exist_ok=True)

    if suffix == ".csv":
        _write_csv(tickets, path)
    elif suffix == ".json":
        _write_json(tickets, path)
    else:
        raise UnsupportedFileFormatError(
            f"Unsupported output format '{suffix}'. Supported: .csv, .json"
        )

    logger.info("Wrote %d ticket(s) to %s", len(tickets), path)


def _write_csv(tickets: list[Ticket], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for t in tickets:
            writer.writerow(t.to_dict())


def _write_json(tickets: list[Ticket], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tickets], f, indent=2)
