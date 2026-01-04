from pathlib import Path

from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()

logger.add(
    LOG_DIR / "shortclick.log",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    encoding="utf-8",
    level="DEBUG",
)

__all__ = ["logger"]
