import logging
import os
from pythonjsonlogger import jsonlogger


def configure_logger(name):
    """
          Configures and returns a logger with specified name and log file.

          This function sets up a logger to write logs to both a file and standard output (console).
          It ensures that each logger is configured only once, even if called multiple times, by checking
          for existing handlers. The log level is set to DEBUG, allowing all log messages to be captured.

          Parameters:
              name (str): The name of the logger. Typically, this would be the name of the module or component.

          Returns:
              logging.Logger: A configured logger instance that writes messages to both the specified log file
              and the console. The logger uses a consistent format for log messages that includes the timestamp,
              logger name, log level, and the log message itself.

          Example:
              >> logger = configure_logger(__name__)
              >> logger.info("This is an info message.")
          """
    logger = logging.getLogger(name)
    log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplication
    if logger.hasHandlers():
        logger.handlers.clear()

    stream_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

