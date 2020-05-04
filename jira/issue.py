import arrow
import attr

from typing import Any, Dict, List, TypeVar, Type
from datetime import datetime

T = TypeVar("T", bound="Parent")


@attr.s
class StatusChange:
    created: datetime = attr.ib()
    status_from: str = attr.ib()
    status_to: str = attr.ib()


@attr.s
class JiraTicket:
    key: str = attr.ib()
    created: datetime = attr.ib()
    updated: datetime = attr.ib()

    status: str = attr.ib()
    changelog: List[StatusChange] = attr.ib()

    @classmethod
    def from_jira_ticket(cls: Type[T], ticket_dict: Dict[str, Dict[str, Any]]) -> T:
        changelog = []
        for item in ticket_dict["changelog"]["histories"]:
            log = item["items"][0]
            if log["field"] != "status":
                continue
            changelog.append(
                StatusChange(
                    created=arrow.get(item["created"]).datetime,
                    status_from=log["fromString"],
                    status_to=log["toString"],
                )
            )

        return cls(
            key=ticket_dict["key"],
            created=arrow.get(ticket_dict["fields"]["created"]).datetime,
            updated=arrow.get(ticket_dict["fields"]["updated"]).datetime,
            status=ticket_dict["fields"]["status"]["name"],
            changelog=changelog,
        )