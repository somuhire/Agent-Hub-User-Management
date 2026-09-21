from dataclasses import dataclass


@dataclass(frozen=True)
class CurrentUser:
    user_id: int
    role: str