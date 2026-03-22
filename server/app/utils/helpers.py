from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get current UTC datetime"""
    return datetime.now(timezone.utc)


def calculate_first_try_rate(first_try_successes: int, total_solved: int) -> float:
    """Calculate first-try success rate"""
    if total_solved == 0:
        return 0.0
    return first_try_successes / total_solved
