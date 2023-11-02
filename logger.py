import logging

class Logger:
    @classmethod
    def get_logger(cls, name: str):
        logger = logging.getLogger(name=name)
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        fh = logging.FileHandler(filename="error.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger


if __name__ == "__main__":
    logger = Logger.get_logger(__name__)
    logger.info("This is a info")
    logger.debug("This is a debug")
    logger.warning("This is a warning")
    logger.error("This is a error")
    logger.critical("This is a critical")