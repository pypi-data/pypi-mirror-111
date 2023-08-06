import logging

from buildblock.decorators import memoized_classproperty


class Loggable:
    """Provide a standard logger for each class"""

    @memoized_classproperty
    def logger(cls):
        return logging.getLogger(cls.__name__)
