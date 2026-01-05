import logging

def configure_logging() -> logging.Logger:
    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logger = logging.getLogger("enqueue-function")
    logging.getLogger("azure").setLevel(logging.WARNING)
    return logger