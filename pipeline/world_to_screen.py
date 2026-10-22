"""View-matrix math: project 3D world coordinates to 2D screen space."""

from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np


@dataclass
class ScreenBox:
    x: int
    y: int
    w: int
    h: int
    distance: float


class WorldToScreen:
    def __init__(self, view_matrix: List[float], screen_w: int, screen_h: int):
        self.matrix = np.array(view_matrix, dtype=np.float64).reshape(4, 4)
        self.screen_w = screen_w
        self.screen_h = screen_h

    def project(self, world: Tuple[float, float, float]) -> Optional[Tuple[float, float]]:
        x, y, z = world
        clip = self.matrix @ np.array([x, y, z, 1.0])
        if clip[3] < 0.001:
            return None
        ndc_x = clip[0] / clip[3]
        ndc_y = clip[1] / clip[3]
        sx = (self.screen_w / 2.0) * (ndc_x + 1.0)
        sy = (self.screen_h / 2.0) * (1.0 - ndc_y)
        return (sx, sy)

    def box_for(self, origin: Tuple[float, float, float], height: float = 72.0) -> Optional[ScreenBox]:
        feet = self.project(origin)
        head = self.project((origin[0], origin[1], origin[2] + height))
        if feet is None or head is None:
            return None
        h = abs(feet[1] - head[1])
        w = h * 0.45
        return ScreenBox(
            x=int(head[0] - w / 2),
            y=int(head[1]),
            w=int(w),
            h=int(h),
            distance=float(np.linalg.norm(origin)),
        )