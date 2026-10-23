"""pyIntradel"""

import logging
from typing import Any

import aiohttp

from . import parser
from .exceptions import AuthenticationError

_LOGGER = logging.getLogger(__name__)
_DATA_URL = "https://www.intradel.be/particulier/data.php"


async def get_data(session: aiohttp.ClientSession, cookie: str) -> list[Any]:
    """Fetch waste collection data.

    `cookie` is the raw `Cookie` header captured from an already logged-in browser session.
    The website gates its login form behind an invisible reCAPTCHA, so the library cannot
    log in by itself.
    """
    _LOGGER.info("Will query data using a session cookie")
    async with session.get(_DATA_URL, headers={"Cookie": cookie}) as resp:
        if resp.status != 200:
            raise ValueError(f"Received error {resp.status}", await resp.text())
        return parser.parse(await resp.text())


__all__ = ["AuthenticationError", "get_data"]
