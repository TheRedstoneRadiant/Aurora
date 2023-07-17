import logging
import sys


def configure_logger(filename):
    logger = logging.getLogger("stdout_logger")
    logger.setLevel(logging.INFO)

    # Create a file handler to write to a text file
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)

    # Create a stream handler to print to console
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)

    # Create a formatter to define the log message format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Set the formatter for both handlers
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Redirect stdout to the logger
    sys.stdout = logger

    return logger
