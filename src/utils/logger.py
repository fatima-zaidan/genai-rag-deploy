import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def get_logger(name: str = __name__, log_file: str = "rag.log") -> logging.Logger:
    """
    Returns a configured logger.
    
    Args:
        name (str): Logger name (usually __name__)
        log_file (str): Log filename inside logs directory

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if already added
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(LOG_DIR / log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(file_formatter)
        logger.addHandler(console_handler)

    return logger
