import logging

logger = logging.getLogger("crypto_paper")


def emit(event: str, **fields) -> None:
    logger.info("PAPER_EVENT %s %s", event, fields)
