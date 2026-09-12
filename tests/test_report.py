from ticket_triage.models import Category, Ticket, Urgency
from ticket_triage.report import summarize


def make_triaged(category, urgency):
    t = Ticket(ticket_id="T-1", subject="s", body="b")
    t.category = category
    t.urgency = urgency
    return t


def test_summarize_counts_by_category_and_urgency():
    tickets = [
        make_triaged(Category.BILLING, Urgency.HIGH),
        make_triaged(Category.BILLING, Urgency.LOW),
        make_triaged(Category.TECHNICAL, Urgency.CRITICAL),
    ]
    summary = summarize(tickets)

    assert summary.total == 3
    assert summary.by_category["billing"] == 2
    assert summary.by_urgency["critical"] == 1
    assert len(summary.critical_tickets) == 1


def test_summarize_as_text_includes_critical_flag():
    tickets = [make_triaged(Category.TECHNICAL, Urgency.CRITICAL)]
    text = summarize(tickets).as_text()
    assert "CRITICAL" in text
