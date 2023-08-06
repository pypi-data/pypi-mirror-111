import logging

class Logger:

    """
    tool for printing debug & warning information
    """

    def logger():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.NOTSET)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s', '%d/%m/%Y %H:%M:%S')
        file_handler = logging.FileHandler('trans.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.WARNING)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger
