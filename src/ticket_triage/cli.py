"""Command-line interface for the ticket triage tool."""

from __future__ import annotations

import argparse
import logging
import sys

from . import __version__
from .exceptions import TicketTriageError
from .export import export_tickets
from .ingest import load_tickets
from .report import summarize
from .triage import triage_all

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ticket-triage",
        description="Analyze a batch of support tickets: categorize, score urgency, and summarize.",
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Path to input tickets file (.csv or .json)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to write triaged tickets (.csv or .json). Optional.",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="Fail on the first malformed ticket record instead of skipping it.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable verbose (DEBUG-level) logging.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    try:
        tickets = load_tickets(args.input, strict=args.strict)
        tickets = triage_all(tickets)
        summary = summarize(tickets)

        print(summary.as_text())

        if args.output:
            export_tickets(tickets, args.output)
            print(f"\nTriaged tickets written to: {args.output}")

        return 0

    except TicketTriageError as exc:
        logger.error(str(exc))
        return 1
    except FileNotFoundError as exc:
        logger.error(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
