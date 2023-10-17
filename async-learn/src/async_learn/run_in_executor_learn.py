import asyncio
from logging import getLogger

import ldap
import requests
from ldap.ldapobject import ReconnectLDAPObject

logger = getLogger()


async def run_requests(url: str, tag: str = ""):
    logger.debug(f"[{tag}] run requests")
    loop = asyncio.get_event_loop()
    try:
        res = await loop.run_in_executor(None, requests.get, url)
    except requests.RequestException as error:
        return error
    logger.debug(f"[{tag}] finish requests")
    return res.url


async def run_ldap(tag: str = ""):
    logger.debug(f"[{tag}] run ldap")
    loop = asyncio.get_event_loop()
    ldap_uri = "ldaps://localhost:1636/"
    ld = ReconnectLDAPObject(ldap_uri, retry_max=3, retry_delay=1)
    try:
        res = await loop.run_in_executor(None, ld.simple_bind_s, "cn=admin", "password")
    except ldap.LDAPError as error:
        return error
    return res


async def run_executor() -> list[asyncio.Future]:
    url = "https://google.com/"
    tasks: list[asyncio.Task] = []
    results: list[asyncio.Future] = []
    try:
        async with asyncio.TaskGroup() as tg:
            for i in range(3):
                tag = f"task {i}"
                tasks.append(tg.create_task(run_requests(url, tag)))
                tasks.append(tg.create_task(run_requests("https://localhost/", tag)))
                tasks.append(tg.create_task(run_ldap(tag)))
        results = [task.result() for task in tasks]
    except* Exception as error:
        logger.error(error.exceptions)
    return results
