import logging
import os
from typing import Optional


def get_logger(name: Optional[str] = None) -> logging.Logger:
  level_name = os.getenv("LOG_LEVEL", "INFO").upper()
  level = getattr(logging, level_name, logging.INFO)
  logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
  logger = logging.getLogger(name if name else __name__)
  logger.setLevel(level)
  return logger


