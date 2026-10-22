"""Walks the entity list and produces normalized player records."""

from dataclasses import dataclass, field
from typing import List, Optional

from utils.logger import get_logger

log = get_logger(__name__)

MAX_ENTITIES = 64
TEAM_RADIANT = 2
TEAM_DIRE = 3


@dataclass
class EntityRecord:
    index: int
    team: int
    hero_id: int
    health: int
    dormant: bool
    origin: tuple = field(default_factory=lambda: (0.0, 0.0, 0.0))


class EntityProcessor:
    def __init__(self, reader, offsets: dict, team_filter: str = "enemy"):
        self.reader = reader
        self.offsets = offsets
        self.team_filter = team_filter

    def _read_int(self, addr: int, offset: str) -> int:
        try:
            return self.reader.read_int(addr + int(self.offsets[offset], 16))
        except Exception:  # noqa: BLE001
            return 0

    def _read_vec3(self, addr: int, offset: str) -> tuple:
        try:
            return self.reader.read_float_vec3(addr + int(self.offsets[offset], 16))
        except Exception:  # noqa: BLE001
            return (0.0, 0.0, 0.0)

    def process(self, snapshot) -> List[EntityRecord]:
        if snapshot is None or snapshot.entity_list_ptr is None:
            return []
        players: List[EntityRecord] = []
        for i in range(MAX_ENTITIES):
            ent = self.reader.read_entity(snapshot.entity_list_ptr, i)
            if not ent:
                continue
            team = self._read_int(ent, "m_iTeamNum")
            if team not in (TEAM_RADIANT, TEAM_DIRE):
                continue
            if self.team_filter == "enemy" and team == self._local_team(snapshot):
                continue
            players.append(EntityRecord(
                index=i,
                team=team,
                hero_id=self._read_int(ent, "m_iHeroID"),
                health=self._read_int(ent, "m_iHealth"),
                dormant=bool(self._read_int(ent, "m_bDormant")),
                origin=self._read_vec3(ent, "m_vecOrigin"),
            ))
        return players

    def _local_team(self, snapshot) -> Optional[int]:
        if snapshot.player_ptr is None:
            return None
        return self._read_int(snapshot.player_ptr, "m_iTeamNum")