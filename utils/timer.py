import time
from contextlib import contextmanager


@contextmanager
def stopwatch(label: str, sink: list):
    start = time.perf_counter()
    try:
        yield
    finally:
        sink.append((label, (time.perf_counter() - start) * 1000.0))


def fps_from_delta(delta_ms: float) -> float:
    return 1000.0 / delta_ms if delta_ms > 0 else 0.0