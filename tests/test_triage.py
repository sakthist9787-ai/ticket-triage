from ticket_triage.models import Category, Ticket, Urgency
from ticket_triage.triage import categorize, score_urgency, triage_ticket


def make_ticket(subject="", body=""):
    return Ticket(ticket_id="T-1", subject=subject, body=body)


def test_categorize_billing():
    t = make_ticket(subject="Refund request", body="I was overcharged on my invoice")
    category, matched = categorize(t)
    assert category == Category.BILLING
    assert "refund" in matched


def test_categorize_shipping():
    t = make_ticket(subject="Where is my package?", body="Tracking hasn't updated in days")
    category, _ = categorize(t)
    assert category == Category.SHIPPING


def test_categorize_defaults_to_general_when_no_keywords_match():
    t = make_ticket(subject="Hello", body="Just saying hi, no issue at all")
    category, matched = categorize(t)
    assert category == Category.GENERAL
    assert matched == []


def test_score_urgency_critical():
    t = make_ticket(subject="Urgent safety issue", body="This is a health risk, please help immediately")
    assert score_urgency(t) == Urgency.CRITICAL


def test_score_urgency_high():
    t = make_ticket(subject="Still not resolved", body="I am very upset, this is unacceptable")
    assert score_urgency(t) == Urgency.HIGH


def test_score_urgency_low_by_default():
    t = make_ticket(subject="Question", body="Just wondering about ingredients")
    assert score_urgency(t) == Urgency.LOW


def test_triage_ticket_sets_all_fields():
    t = make_ticket(subject="Urgent refund needed", body="Overcharged, need this fixed immediately")
    triaged = triage_ticket(t)
    assert triaged.category == Category.BILLING
    assert triaged.urgency == Urgency.CRITICAL
    assert "refund" in triaged.matched_keywords
