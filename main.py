"""dota2-external-esp entry point.

Educational external ESP for Dota 2 — read-only overlay.
Use only in private lobbies / offline practice. See SECURITY.md.
"""

import json
import sys
import time
from pathlib import Path

from pipeline.ingest_worker import IngestWorker
from pipeline.entity_processor import EntityProcessor
from pipeline.world_to_screen import WorldToScreen
from drivers.overlay_driver import OverlayDriver
from drivers.console_driver import ConsoleDriver
from services.hero_service import HeroService
from state.session import SessionState
from utils.logger import get_logger

log = get_logger(__name__)
ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    settings = load_json(ROOT / "config" / "settings.json")
    offsets = load_json(ROOT / "config" / "offsets.json")["offsets"]

    hero_svc = HeroService()
    ingest = IngestWorker(settings["process_name"], offsets,
                          settings["poll_interval_ms"])
    if not ingest.attach():
        log.error("could not attach — is Dota 2 running?")
        return 1

    processor = EntityProcessor(ingest, offsets,
                                settings["esp"]["team_filter"])
    overlay = OverlayDriver(1920, 1080, settings["esp"]["font_size"])
    console = ConsoleDriver(enabled=False)
    state = SessionState(running=True)

    log.info("pipeline running — press Ctrl+C to stop")
    try:
        while state.running:
            snap = ingest.poll()
            if snap is None:
                continue
            players = processor.process(snap)
            state.advance(players)

            overlay.begin_frame()
            for p in players:
                if p.dormant:
                    continue
                box = None
                if box is None:
                    continue
                overlay.draw_player(box, hero_svc.name_of(p.hero_id), p.health)
            overlay.end_frame()
            time.sleep(0.001)
    except KeyboardInterrupt:
        log.info("interrupted by user")
    finally:
        overlay.shutdown()
        console.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())