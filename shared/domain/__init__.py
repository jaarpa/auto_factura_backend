from datetime import datetime
from datetime import UTC


def utc_now() -> datetime:
    """
    Returns current UTC time
    """
    return datetime.now(UTC)
