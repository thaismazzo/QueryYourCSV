import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
    handlers=[
        logging.StreamHandler()                                   
    ]
)

def get_logger(name: str):
    """
    Returns a named logger for the module or script.

    Parameters:
        name (str): Name of the logger, usually __name__.

    Returns:
        logging.Logger: Configured logger instance to be used for logging messages.
    """
    return logging.getLogger(name)