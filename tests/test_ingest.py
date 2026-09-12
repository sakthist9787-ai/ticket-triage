import json

import pytest

from ticket_triage.exceptions import (
    EmptyDatasetError,
    UnsupportedFileFormatError,
)
from ticket_triage.ingest import load_tickets


def test_load_tickets_from_json(tmp_path):
    data = {"tickets": [{"ticket_id": "T-1", "subject": "s", "body": "b"}]}
    path = tmp_path / "tickets.json"
    path.write_text(json.dumps(data))

    tickets = load_tickets(path)
    assert len(tickets) == 1
    assert tickets[0].ticket_id == "T-1"


def test_load_tickets_from_csv(tmp_path):
    path = tmp_path / "tickets.csv"
    path.write_text("ticket_id,subject,body\nT-1,Subj,Body text\n")

    tickets = load_tickets(path)
    assert len(tickets) == 1
    assert tickets[0].subject == "Subj"


def test_load_tickets_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_tickets(tmp_path / "does_not_exist.csv")


def test_load_tickets_unsupported_format_raises(tmp_path):
    path = tmp_path / "tickets.txt"
    path.write_text("nonsense")
    with pytest.raises(UnsupportedFileFormatError):
        load_tickets(path)


def test_load_tickets_skips_malformed_records_by_default(tmp_path):
    data = {
        "tickets": [
            {"ticket_id": "T-1", "subject": "s", "body": "b"},
            {"ticket_id": "", "subject": "s", "body": "b"},  # malformed
        ]
    }
    path = tmp_path / "tickets.json"
    path.write_text(json.dumps(data))

    tickets = load_tickets(path)
    assert len(tickets) == 1


def test_load_tickets_strict_raises_on_malformed(tmp_path):
    data = {"tickets": [{"ticket_id": "", "subject": "s", "body": "b"}]}
    path = tmp_path / "tickets.json"
    path.write_text(json.dumps(data))

    with pytest.raises(Exception):
        load_tickets(path, strict=True)


def test_load_tickets_empty_dataset_raises(tmp_path):
    data = {"tickets": []}
    path = tmp_path / "tickets.json"
    path.write_text(json.dumps(data))

    with pytest.raises(EmptyDatasetError):
        load_tickets(path)
