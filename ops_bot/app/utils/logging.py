import logging
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
  logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
  )
  return logging.getLogger(name if name else __name__)


