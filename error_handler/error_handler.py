from datetime import datetime


def log_handler(exception: Exception, action: str) -> str:
    """
    Builds the proper log message according to the exception and action retrieved.
    :param exception: error message caught
    :param action: identifies the caller of this method
    :return: string that represent the composed log message
    """
    return "{} - {} exception has been thrown on {} -> {}"\
        .format(datetime.now().strftime("%d-%m-%y %H:%M:%S"), type(exception), action, exception)
