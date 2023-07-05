import logging

def setup_logger(logger):
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler("log.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
