import pytest

from ticket_triage.exceptions import InvalidTicketDataError
from ticket_triage.models import Category, Ticket, Urgency


def test_ticket_from_dict_success():
    raw = {"ticket_id": "T-1", "subject": "Help", "body": "Something broke"}
    t = Ticket.from_dict(raw)
    assert t.ticket_id == "T-1"
    assert t.subject == "Help"
    assert t.category == Category.GENERAL
    assert t.urgency == Urgency.LOW


def test_ticket_from_dict_strips_whitespace():
    raw = {"ticket_id": "  T-2 ", "subject": " Subject ", "body": " Body "}
    t = Ticket.from_dict(raw)
    assert t.ticket_id == "T-2"
    assert t.subject == "Subject"
    assert t.body == "Body"


@pytest.mark.parametrize("missing_field", ["ticket_id", "subject", "body"])
def test_ticket_from_dict_missing_required_field_raises(missing_field):
    raw = {"ticket_id": "T-1", "subject": "Help", "body": "Something broke"}
    raw[missing_field] = ""
    with pytest.raises(InvalidTicketDataError):
        Ticket.from_dict(raw)


def test_ticket_to_dict_roundtrip_fields():
    t = Ticket(ticket_id="T-1", subject="s", body="b", customer="c", created_at="2026-01-01")
    t.category = Category.BILLING
    t.urgency = Urgency.HIGH
    t.matched_keywords = ["refund"]

    d = t.to_dict()
    assert d["category"] == "billing"
    assert d["urgency"] == "high"
    assert d["matched_keywords"] == "refund"
