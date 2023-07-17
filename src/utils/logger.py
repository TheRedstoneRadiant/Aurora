import logging
import sys
import io


class StreamToLogger(io.TextIOBase):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.line_buffer = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass


def configure_logger(filename):
    logger = logging.getLogger("stdout_logger")
    logger.setLevel(logging.INFO)

    # Create a file handler to write to a text file
    file_handler = logging.FileHandler(filename, mode="w")
    file_handler.setLevel(logging.INFO)

    # Create a stream handler to print to console
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # Redirect stdout to the logger
    sys.stdout = StreamToLogger(logger)

    return logger
