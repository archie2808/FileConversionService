import logging

def configure_logger(name, log_file='app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent adding multiple handlers to the logger if it's already configured
    if not logger.handlers:
        # File handler - logs to a file
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)



        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    return logger

