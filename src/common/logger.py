import logging


def create_logger(name='PYTHON_WTP_QA', level='DEBUG'):
    logger_ = logging.getLogger() if name is None else logging.getLogger(name)
    logger_.setLevel(level)
    format_ = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger_.addHandler(console_handler)
    return logger_


logger = create_logger()
