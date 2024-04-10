import logging


def configure_logger(name, log_file='app.log'):
    """
    Configures and returns a logger with specified name and log file.

    This function sets up a logger to write logs to both a file and standard output (console).
    It ensures that each logger is configured only once, even if called multiple times, by checking
    for existing handlers. The log level is set to DEBUG, allowing all log messages to be captured.

    Parameters:
        name (str): The name of the logger. Typically, this would be the name of the module or component.
        log_file (str, optional): The path to the log file where log messages will be written. Defaults to 'app.log'.

    Returns:
        logging.Logger: A configured logger instance that writes messages to both the specified log file
        and the console. The logger uses a consistent format for log messages that includes the timestamp,
        logger name, log level, and the log message itself.

    Example:
        >> logger = configure_logger(__name__)
        >> logger.info("This is an info message.")
        # This message will be written to 'app.log' and printed to the console.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set log level to DEBUG to capture all types of log messages.

    # Check if the logger already has handlers to prevent adding them multiple times.
    if not logger.handlers:
        # Set up writing logs to a file.
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Set up writing logs to the console.
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    return logger
