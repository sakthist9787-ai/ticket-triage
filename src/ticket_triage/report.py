"""Summary reporting for triaged tickets."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from .models import Ticket, Urgency


@dataclass
class Summary:
    total: int
    by_category: Counter
    by_urgency: Counter
    critical_tickets: list[Ticket]

    def as_text(self) -> str:
        lines = [
            "=" * 50,
            "SUPPORT TICKET TRIAGE SUMMARY",
            "=" * 50,
            f"Total tickets analyzed: {self.total}",
            "",
            "By category:",
        ]
        for category, count in self.by_category.most_common():
            lines.append(f"  {category:<18} {count}")

        lines.append("")
        lines.append("By urgency:")
        for urgency in (Urgency.CRITICAL, Urgency.HIGH, Urgency.MEDIUM, Urgency.LOW):
            count = self.by_urgency.get(urgency.value, 0)
            lines.append(f"  {urgency.value:<18} {count}")

        if self.critical_tickets:
            lines.append("")
            lines.append(f"⚠ {len(self.critical_tickets)} CRITICAL ticket(s) require immediate attention:")
            for t in self.critical_tickets:
                lines.append(f"  - [{t.ticket_id}] {t.subject}")

        lines.append("=" * 50)
        return "\n".join(lines)


def summarize(tickets: list[Ticket]) -> Summary:
    """Build a Summary from a list of triaged tickets."""
    by_category = Counter(t.category.value for t in tickets)
    by_urgency = Counter(t.urgency.value for t in tickets)
    critical = [t for t in tickets if t.urgency == Urgency.CRITICAL]

    return Summary(
        total=len(tickets),
        by_category=by_category,
        by_urgency=by_urgency,
        critical_tickets=critical,
    )
