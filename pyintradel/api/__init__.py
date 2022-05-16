"""pyIntradel"""

import logging
from typing import Any

import aiohttp

from . import parser
from . import towns

logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s: %(message)s")

_LOGGER = logging.getLogger(__name__)
_URL = "https://www.intradel.be/particulier/"
_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}


async def get_data(
    session: aiohttp.ClientSession, login: str, password: str, town: str
) -> list[Any]:
    _LOGGER.info("Will query data for user %s and city %s", login, town)

    town_id = towns.TOWNS_MAP.get(town.upper())
    if not town_id:
        ValueError("Town not found", town)

    data = {"llogin": "YES", "login": login, "pass": password, "commune": town_id}

    async with session.post(_URL, data=data, headers=_HEADERS) as resp:
        if resp.status != 200:
            raise ValueError(f"Received error {resp.status}", await resp.text())
        else:
            return parser.parse(await resp.text())
