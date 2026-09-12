"""Core triage logic: categorization and urgency scoring for tickets."""

from __future__ import annotations

from .models import Category, Ticket, Urgency

# Keyword -> category mapping. Order matters only in that a ticket is assigned
# to the first category with a keyword match; ties favor the earlier category.
CATEGORY_KEYWORDS: dict[Category, list[str]] = {
    Category.BILLING: [
        "invoice", "charge", "refund", "billing", "payment", "subscription",
        "overcharged", "credit card", "receipt",
    ],
    Category.SHIPPING: [
        "shipping", "delivery", "tracking", "package", "shipment", "delayed",
        "lost package", "courier",
    ],
    Category.PRODUCT_QUALITY: [
        "broken", "defective", "damaged", "moldy", "spoiled", "expired",
        "wrong item", "quality issue", "leaking",
    ],
    Category.TECHNICAL: [
        "error", "bug", "crash", "not working", "login", "password", "app",
        "website", "404", "glitch",
    ],
    Category.ACCOUNT: [
        "account", "cancel", "unsubscribe", "delete my data", "email change",
        "profile",
    ],
}

# Urgency keywords, highest priority first.
URGENCY_KEYWORDS: dict[Urgency, list[str]] = {
    Urgency.CRITICAL: [
        "urgent", "emergency", "immediately", "asap", "allergic reaction",
        "health risk", "legal action", "lawsuit", "safety",
    ],
    Urgency.HIGH: [
        "very upset", "angry", "unacceptable", "third time", "still not resolved",
        "no response", "escalate",
    ],
    Urgency.MEDIUM: [
        "disappointed", "please help", "issue", "problem", "not happy",
    ],
}


def categorize(ticket: Ticket) -> tuple[Category, list[str]]:
    """Determine the category for a ticket and which keywords matched."""
    text = f"{ticket.subject} {ticket.body}".lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        matched = [kw for kw in keywords if kw in text]
        if matched:
            return category, matched

    return Category.GENERAL, []


def score_urgency(ticket: Ticket) -> Urgency:
    """Determine urgency level for a ticket based on keyword signals."""
    text = f"{ticket.subject} {ticket.body}".lower()

    for urgency, keywords in URGENCY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return urgency

    return Urgency.LOW


def triage_ticket(ticket: Ticket) -> Ticket:
    """Run categorization and urgency scoring on a single ticket, in place."""
    category, matched = categorize(ticket)
    ticket.category = category
    ticket.matched_keywords = matched
    ticket.urgency = score_urgency(ticket)
    return ticket


def triage_all(tickets: list[Ticket]) -> list[Ticket]:
    """Run triage on a list of tickets."""
    return [triage_ticket(t) for t in tickets]
