from logging import Logger


def safe_run(logger: Logger = None):
    def wrapper(func):
        def inner(*arg, **kwargs):
            try:
                res = func(*arg, **kwargs)
                return res, None
            except Exception as e:
                if logger:
                    logger.exception(e)
                return None, e

        return inner

    return wrapper
