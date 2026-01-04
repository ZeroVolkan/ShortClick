from datetime import datetime, timezone
from urllib.parse import urlparse


def nowtime():
    return datetime.now(timezone.utc)


def check_url(url: str) -> bool:
    if not url:
        return False

    try:
        parsed = urlparse(url)
    except Exception:
        return False

    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.hostname == "localhost"
        or parsed.hostname.startswith("127.")
    ):
        return False

    return True
