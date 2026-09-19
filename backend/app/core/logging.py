import logging
import sys
import os
from logging.handlers import RotatingFileHandler

# Create a logs folder in the root directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

def get_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs if the logger is called multiple times
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
        )

        # 1. Terminal Output Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 2. File Output Handler (Max 5MB per file, keep 3 backups)
        file_handler = RotatingFileHandler(
            "logs/pipeline.log", 
            maxBytes=5_000_000, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger