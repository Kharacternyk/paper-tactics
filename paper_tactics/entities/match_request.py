from dataclasses import dataclass


@dataclass
class MatchRequest:
    id: str
    view_data: dict[str, str]
