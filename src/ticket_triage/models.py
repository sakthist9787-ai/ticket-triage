"""Data models for support tickets."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Category(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    SHIPPING = "shipping"
    PRODUCT_QUALITY = "product_quality"
    ACCOUNT = "account"
    GENERAL = "general"


class Urgency(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


REQUIRED_FIELDS = {"ticket_id", "subject", "body"}


@dataclass
class Ticket:
    """A single support ticket, with derived triage fields populated after analysis."""

    ticket_id: str
    subject: str
    body: str
    customer: str = ""
    created_at: str = ""

    category: Category = Category.GENERAL
    urgency: Urgency = Urgency.LOW
    matched_keywords: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict) -> "Ticket":
        """Build a Ticket from a raw dict (e.g. a parsed CSV/JSON row).

        Raises:
            InvalidTicketDataError: if required fields are missing or empty.
        """
        from .exceptions import InvalidTicketDataError

        missing = REQUIRED_FIELDS - {k for k, v in raw.items() if v not in (None, "")}
        if missing:
            raise InvalidTicketDataError(
                f"Ticket record missing required field(s): {sorted(missing)} -> {raw}"
            )

        return cls(
            ticket_id=str(raw["ticket_id"]).strip(),
            subject=str(raw["subject"]).strip(),
            body=str(raw["body"]).strip(),
            customer=str(raw.get("customer", "")).strip(),
            created_at=str(raw.get("created_at", "")).strip(),
        )

    def to_dict(self) -> dict:
        """Serialize the ticket (including derived fields) back to a plain dict."""
        return {
            "ticket_id": self.ticket_id,
            "subject": self.subject,
            "body": self.body,
            "customer": self.customer,
            "created_at": self.created_at,
            "category": self.category.value,
            "urgency": self.urgency.value,
            "matched_keywords": ", ".join(self.matched_keywords),
        }
