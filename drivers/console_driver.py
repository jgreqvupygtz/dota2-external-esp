"""Debug console output driver for headless / CI runs."""

from typing import List

from utils.logger import get_logger

log = get_logger(__name__)


class ConsoleDriver:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._frames = 0

    def begin_frame(self):
        self._frames += 1

    def draw_player(self, box, hero_name: str, health: int):
        if not self.enabled:
            return
        log.info("frame=%d hero=%s hp=%d pos=(%d,%d) dist=%.0f",
                 self._frames, hero_name, health, box.x, box.y, box.distance)

    def end_frame(self):
        pass

    def shutdown(self):
        log.info("console driver stopped after %d frames", self._frames)