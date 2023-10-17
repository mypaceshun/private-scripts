import asyncio
from logging import getLogger

logger = getLogger()


async def async_func():
    logger.info("async func")
    logger.info(asyncio.iscoroutinefunction(async_func))


def func():
    logger.info("func")
    logger.info(asyncio.iscoroutinefunction(func))
