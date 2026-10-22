"""Attaches to dota2.exe and pulls raw snapshots from process memory."""

import time
import logging
from dataclasses import dataclass
from typing import Optional

import pymem
from pymem.process import module_from_name

from utils.logger import get_logger

log = get_logger(__name__)


@dataclass
class MemorySnapshot:
    tick: int
    timestamp: float
    player_ptr: Optional[int]
    entity_list_ptr: Optional[int]
    view_matrix_addr: Optional[int]


class IngestWorker:
    def __init__(self, process_name: str, offsets: dict, poll_ms: int = 16):
        self.process_name = process_name
        self.offsets = offsets
        self.poll_ms = poll_ms
        self._pm: Optional[pymem.Pymem] = None
        self._client_base: Optional[int] = None
        self._tick = 0

    def attach(self) -> bool:
        try:
            self._pm = pymem.Pymem(self.process_name)
            module = module_from_name(self._pm.process_handle, "client.dll")
            self._client_base = module.lpBaseOfDll
            log.info("attached to %s client.dll @ 0x%X",
                     self.process_name, self._client_base)
            return True
        except Exception as exc:  # noqa: BLE001
            log.error("attach failed: %s", exc)
            return False

    def _read_ptr(self, offset: str) -> Optional[int]:
        if self._pm is None or self._client_base is None:
            return None
        try:
            return self._pm.read_longlong(self._client_base + int(self.offsets[offset], 16))
        except Exception:  # noqa: BLE001
            return None

    def poll(self) -> Optional[MemorySnapshot]:
        if self._pm is None:
            return None
        self._tick += 1
        snap = MemorySnapshot(
            tick=self._tick,
            timestamp=time.time(),
            player_ptr=self._read_ptr("dwLocalPlayer"),
            entity_list_ptr=self._read_ptr("dwEntityList"),
            view_matrix_addr=None,
        )
        time.sleep(self.poll_ms / 1000.0)
        return snap