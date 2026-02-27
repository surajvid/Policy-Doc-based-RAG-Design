"""
logging.py

Non-technical explanation:
- Logging is like keeping a "black box recorder" for the app.
- When something goes wrong, logs help us see what happened.

For now, we keep it very simple.
"""

import logging


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
