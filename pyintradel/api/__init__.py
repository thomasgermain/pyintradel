"""pyIntradel"""

import logging
import re
from http.cookies import CookieError, SimpleCookie
from typing import Any

import aiohttp

from . import parser
from .exceptions import ApiError, AuthenticationError, IntradelError, ParseError

_LOGGER = logging.getLogger(__name__)
_DATA_URL = "https://www.intradel.be/particulier/data.php"
# Case-insensitive: HTTP/2 dev tools show the header name lowercased.
_COOKIE_HEADER_PREFIX = re.compile(r"^\s*cookie\s*:", re.IGNORECASE)


async def get_data(session: aiohttp.ClientSession, cookie: str) -> list[Any]:
    """Fetch waste collection data.

    `cookie` is the raw `Cookie` header captured from an already logged-in browser session.
    The website gates its login form behind an invisible reCAPTCHA, so the library cannot
    log in by itself.
    """
    cookies = _parse_cookie(cookie)
    if not cookies:
        raise AuthenticationError()

    _LOGGER.info("Will query data using a session cookie")
    # Passed as `cookies`, not as a Cookie header: aiohttp lets cookies stored in the session's
    # jar override a hand-written header, and intradel sets an anonymous PHPSESSID on any request
    # without a session, so a shared session would otherwise send that one instead.
    async with session.get(_DATA_URL, cookies=cookies, allow_redirects=False) as resp:
        # Intradel redirects to its login page when the session is not valid.
        if resp.status == 302:
            raise AuthenticationError()
        if resp.status != 200:
            if _LOGGER.isEnabledFor(logging.DEBUG):
                # Lenient decoding: an error page in an odd charset must not mask the ApiError.
                body = await resp.text(errors="replace")
                _LOGGER.debug("HTTP %s body: %s", resp.status, body)
            raise ApiError(resp.status)
        return parser.parse(await resp.text())


def _parse_cookie(cookie: str) -> dict[str, str]:
    """Parse the cookie as copied from browser dev tools, e.g. "Cookie: PHPSESSID=...\\n"."""
    try:
        parsed = SimpleCookie(_COOKIE_HEADER_PREFIX.sub("", cookie))
    except CookieError:
        return {}
    return {name: morsel.value for name, morsel in parsed.items()}


__all__ = ["ApiError", "AuthenticationError", "IntradelError", "ParseError", "get_data"]
