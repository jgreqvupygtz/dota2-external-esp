"""Pygame-based transparent overlay window that draws ESP boxes."""

import pygame

from utils.logger import get_logger

log = get_logger(__name__)

COLOR_ENEMY = (255, 64, 64)
COLOR_TEAM = (64, 200, 255)
COLOR_HEALTH = (80, 255, 120)


class OverlayDriver:
    def __init__(self, width: int, height: int, font_size: int = 12):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (width, height), pygame.NOFRAME | pygame.SRCALPHA
        )
        self.font = pygame.font.SysFont("Consolas", font_size)
        log.info("overlay initialized %dx%d", width, height)

    def begin_frame(self):
        self.screen.fill((0, 0, 0, 0))

    def draw_player(self, box, hero_name: str, health: int):
        color = COLOR_ENEMY
        pygame.draw.rect(self.screen, color, (box.x, box.y, box.w, box.h), 1)
        bar_w = box.w
        bar_h = max(2, int(box.h * 0.06))
        hp_frac = max(0.0, min(1.0, health / 1000.0))
        pygame.draw.rect(self.screen, COLOR_HEALTH,
                         (box.x, box.y + box.h + 2, int(bar_w * hp_frac), bar_h))
        label = self.font.render(f"{hero_name} [{int(box.distance)}m]", True, color)
        self.screen.blit(label, (box.x, box.y - 14))

    def end_frame(self):
        pygame.display.flip()

    def shutdown(self):
        pygame.quit()
        log.info("overlay shutdown")