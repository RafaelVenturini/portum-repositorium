import time


def easy_time(ms: int) -> str:
    total_seconds = ms // 1000

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    parts = []

    if hours:
        parts.append(f"{hours}h")

    if minutes:
        parts.append(f"{minutes}m")

    if seconds or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


def elapsed_time(start_time: float) -> str:
    elapsed_ms = int((time.perf_counter() - start_time) * 1000)
    return easy_time(elapsed_ms)
