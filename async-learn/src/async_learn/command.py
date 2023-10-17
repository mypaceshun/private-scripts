import asyncio
from logging import Formatter, basicConfig, getLogger

import click
from rich.logging import RichHandler

from async_learn import __name__, __version__
from async_learn.run_in_executor_learn import run_executor

FORMAT = "%(message)s"
FORMAT_TRACE = "%(message)s (%(pathname)s:%(lineno)d:%(funcName)s)"
basicConfig(level="WARNING", format=FORMAT, handlers=[RichHandler()])
logger = getLogger()


def verbose_logger(ctx, param, value):
    if not isinstance(value, int):
        return value
    default_level = "DEBUG"
    if value == 0:
        logger.setLevel(default_level)
    if value == 1:
        logger.setLevel("INFO")
    if value == 2:
        logger.setLevel("DEBUG")
    if value >= 3:
        logger.setLevel("DEBUG")
        logger.handlers[0].setFormatter(Formatter(FORMAT_TRACE))


@click.command()
@click.option(
    "-v", "--verbose", help="verbose output", count=True, callback=verbose_logger
)
@click.version_option(__version__, "-V", "--version", package_name=__name__)
@click.help_option("-h", "--help")
def cli(verbose):
    logger.warning("WARNING")
    logger.info("INFO")
    logger.debug("DEBUG")
    res = asyncio.run(run_executor())
    logger.debug(f"{res=}")
