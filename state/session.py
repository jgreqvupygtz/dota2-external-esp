from dataclasses import dataclass, field
from typing import Dict, List

from pipeline.entity_processor import EntityRecord


@dataclass
class SessionState:
    running: bool = False
    frame: int = 0
    last_snapshot_tick: int = 0
    players: List[EntityRecord] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)

    def advance(self, players: List[EntityRecord]):
        self.frame += 1
        self.players = players
        self.metrics["players"] = float(len(players))