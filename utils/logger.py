import logging
from pathlib import Path


def get_logger(logger_name):
    project_root = Path(__file__).resolve().parent.parent
    log_directory = project_root / "logs"
    log_directory.mkdir(exist_ok=True)

    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # File Handler
        file_handler = logging.FileHandler(
            log_directory / "api_automation.log",
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger