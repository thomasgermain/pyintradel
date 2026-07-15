"""pyIntradel"""

import logging
from typing import Any

import aiohttp

from . import parser, towns

_LOGGER = logging.getLogger(__name__)
_URL = "https://www.intradel.be/particulier/"
_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}


async def get_data(
    session: aiohttp.ClientSession,
    login: str | None = None,
    password: str | None = None,
    town: str | None = None,
    *,
    cookie: str | None = None,
) -> list[Any]:
    """Fetch waste collection data.

    Authenticate either with `login`, `password` and `town`, or with a `cookie`
    (the raw `Cookie` header captured from an already logged-in browser session).
    The website now gates the login form behind an invisible reCAPTCHA, so a plain
    login/password POST can be rejected; the cookie skips the login step entirely.
    """
    if cookie:
        _LOGGER.info("Will query data using a session cookie")
        headers = {"Cookie": cookie}

        async with session.get(
            "https://www.intradel.be/particulier/data.php", headers=headers
        ) as resp:
            if resp.status != 200:
                raise ValueError(f"Received error {resp.status}", await resp.text())
            return parser.parse(await resp.text())

    if not login or not password or not town:
        raise ValueError("Either 'cookie' or 'login', 'password' and 'town' must be provided")

    town_id = towns.TOWNS_MAP.get(town.upper())
    if not town_id:
        raise ValueError("Town not found", town)

    _LOGGER.info("Will query data for user %s and city %s", login, town)
    data = {"llogin": "YES", "login": login, "pass": password, "commune": town_id}

    async with session.post(_URL, data=data, headers=_HEADERS) as resp:
        if resp.status != 200:
            raise ValueError(f"Received error {resp.status}", await resp.text())
        else:
            return parser.parse(await resp.text())
