import uuid
from datetime import datetime, timezone


def nowtime():
    return datetime.now(timezone.utc)


def generate_short_url() -> str:
    return str(uuid.uuid4().hex[:20])
