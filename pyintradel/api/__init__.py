"""pyIntradel"""

import logging
from typing import Any

import aiohttp

from . import parser
from .exceptions import ApiError, AuthenticationError, IntradelError, ParseError

_LOGGER = logging.getLogger(__name__)
_DATA_URL = "https://www.intradel.be/particulier/data.php"
# Enough of an error page to diagnose it, without flooding the logs.
_MAX_LOGGED_BODY = 500


async def get_data(session: aiohttp.ClientSession, cookie: str) -> list[Any]:
    """Fetch waste collection data.

    `cookie` is the raw `Cookie` header captured from an already logged-in browser session.
    The website gates its login form behind an invisible reCAPTCHA, so the library cannot
    log in by itself.
    """
    _LOGGER.info("Will query data using a session cookie")
    async with session.get(_DATA_URL, headers={"Cookie": cookie}) as resp:
        body = await resp.text()
        if resp.status != 200:
            _LOGGER.debug("HTTP %s body: %s", resp.status, body[:_MAX_LOGGED_BODY])
            raise ApiError(resp.status)
        return parser.parse(body)


__all__ = ["ApiError", "AuthenticationError", "IntradelError", "ParseError", "get_data"]
