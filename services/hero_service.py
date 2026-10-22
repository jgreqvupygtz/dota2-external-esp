"""Loads hero id -> name/icon mapping used by the overlay labels."""

import json
from pathlib import Path
from typing import Dict, Optional

from utils.logger import get_logger

log = get_logger(__name__)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "heroes.json"


class HeroService:
    def __init__(self, path: Path = DATA_PATH):
        self.path = path
        self._heroes: Dict[int, dict] = {}
        self._load()

    def _load(self):
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self._heroes = {int(k): v for k, v in raw.items()}
            log.info("loaded %d heroes", len(self._heroes))
        except FileNotFoundError:
            log.warning("heroes.json missing at %s", self.path)

    def name_of(self, hero_id: int) -> str:
        return self._heroes.get(hero_id, {}).get("name", f"hero_{hero_id}")

    def icon_of(self, hero_id: int) -> Optional[str]:
        return self._heroes.get(hero_id, {}).get("icon")