from dataclasses import dataclass
from typing import Optional

@dataclass
class BriefSession:
    user_id: int
    brief_id: str
    last_fragment_index: int
    started_at: str
    status: str = "active"

    def next_fragment_index(self) -> int:
        return self.last_fragment_index + 1

    def mark_done(self):
        self.status = "done"