import asyncio
from logging import getLogger
from time import sleep

logger = getLogger()


def func(future: asyncio.futures.Future, tag: str, num: int = 3):
    logger.debug(f"[{tag}] run")
    for i in range(num):
        sleep(1)
        logger.debug(f"[{tag}] sleep {i+1}/{num}")
    logger.debug(f"[{tag}] Finish")
    future.set_result(f"[{tag}] Finish")
    return


def yield_func(tag: str, num: int = 3):
    logger.debug(f"[{tag}] run")
    yield
    for i in range(num):
        sleep(1)
        logger.debug(f"[{tag}] sleep {i+1}/{num}")
    logger.debug(f"[{tag}] Finish")
    return


def event_loop_run() -> None:
    loop = asyncio.get_event_loop()
    futures: list[asyncio.futures.Future] = []
    num = 3
    for i in range(num):
        tag = f"future {i:2}"
        future = loop.create_future()
        loop.call_soon(func, future, tag, 2)
        futures.append(future)
    res = loop.run_until_complete(asyncio.gather(*futures))
    logger.debug(f"{res=}")

    tasks = []
    for i in range(num):
        tag = f"yield {i:2}"
        task = yield_func(tag)
        tasks.append(task)
    res = loop.run_until_complete(asyncio.gather(*tasks))
    logger.debug(f"{res=}")
    return res
