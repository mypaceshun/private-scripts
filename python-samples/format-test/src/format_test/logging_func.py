from logging import NullHandler, getLogger

from format_test.decorators import benchmark

logger = getLogger(__name__)
logger.addHandler(NullHandler())


@benchmark
def logging_run(num: int = 100):
    for i in range(num):
        logger.info("test %d and %s", i, "text")
