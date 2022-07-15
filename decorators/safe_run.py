from distutils.log import error


def safe_run(logger=None):
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
