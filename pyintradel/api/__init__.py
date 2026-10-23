"""pyIntradel"""

import logging
import re
from typing import Any

import aiohttp

from . import parser
from .exceptions import ApiError, AuthenticationError, IntradelError, ParseError

_LOGGER = logging.getLogger(__name__)
_DATA_URL = "https://www.intradel.be/particulier/data.php"
# Enough of an error page to diagnose it, without flooding the logs.
_MAX_LOGGED_BODY = 500
# Case-insensitive: HTTP/2 dev tools show the header name lowercased.
_COOKIE_HEADER_PREFIX = re.compile(r"^\s*cookie\s*:", re.IGNORECASE)


async def get_data(session: aiohttp.ClientSession, cookie: str) -> list[Any]:
    """Fetch waste collection data.

    `cookie` is the raw `Cookie` header captured from an already logged-in browser session.
    The website gates its login form behind an invisible reCAPTCHA, so the library cannot
    log in by itself.
    """
    _LOGGER.info("Will query data using a session cookie")
    headers = {"Cookie": _normalize_cookie(cookie)}
    async with session.get(_DATA_URL, headers=headers, allow_redirects=False) as resp:
        # Intradel redirects to its login page when the session is not valid.
        if resp.status == 302:
            raise AuthenticationError()
        if resp.status != 200:
            if _LOGGER.isEnabledFor(logging.DEBUG):
                # Lenient decoding: an error page in an odd charset must not mask the ApiError.
                body = await resp.text(errors="replace")
                _LOGGER.debug("HTTP %s body: %s", resp.status, body[:_MAX_LOGGED_BODY])
            raise ApiError(resp.status)
        return parser.parse(await resp.text())


def _normalize_cookie(cookie: str) -> str:
    """Accept the cookie as copied from browser dev tools, e.g. "Cookie: PHPSESSID=...\\n"."""
    return _COOKIE_HEADER_PREFIX.sub("", cookie).strip()


__all__ = ["ApiError", "AuthenticationError", "IntradelError", "ParseError", "get_data"]
