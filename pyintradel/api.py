import asyncio
import logging
import sys
from typing import Any

import aiohttp

from pyintradel.towns import TOWNS_MAP
from pyintradel.parser import parse

_LOGGER = logging.getLogger(__name__)
_URL = "https://www.intradel.be/particulier/"
_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}


async def get_data(
    session: aiohttp.ClientSession, login: str, password: str, town: str
) -> list[Any]:
    _LOGGER.info("Will query data for user %s and city %s", login, town)

    town_id = TOWNS_MAP.get(town.upper())
    if not town_id:
        ValueError("Town not found", town)

    data = {"llogin": "YES", "login": login, "pass": password, "commune": town_id}

    async with session.post(_URL, data=data, headers=_HEADERS) as resp:
        if resp.status != 200:
            raise ValueError(f"Received error {resp.status}", await resp.text())
        else:
            return parse(await resp.text())


async def _main(login: str, password: str, town: str) -> list[Any]:
    async with aiohttp.ClientSession() as sess:
        return await get_data(sess, login, password, town)


if __name__ == "__main__":
    if not len(sys.argv) == 4:
        print("Usage: python3 api.py user pass town")
        sys.exit(0)
    user_param = sys.argv[1]
    passw_param = sys.argv[2]
    town_param = sys.argv[3]

    asyncio.get_event_loop().run_until_complete(_main(user_param, passw_param, town_param))
