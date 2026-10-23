"""pyIntradel"""

import logging
import re
from typing import Any

import aiohttp

from . import parser
from .exceptions import ApiError, AuthenticationError, IntradelError, ParseError

_LOGGER = logging.getLogger(__name__)
_DATA_URL = "https://www.intradel.be/particulier/data.php"
# Registrable domain, so cookies set for the host or for the whole domain are both covered.
_COOKIE_DOMAIN = "intradel.be"
# Case-insensitive: HTTP/2 dev tools show the header name lowercased.
_COOKIE_HEADER_PREFIX = re.compile(r"^\s*cookie\s*:", re.IGNORECASE)


async def get_data(session: aiohttp.ClientSession, cookie: str) -> list[Any]:
    """Fetch waste collection data.

    `cookie` is the raw `Cookie` header captured from an already logged-in browser session.
    The website gates its login form behind an invisible reCAPTCHA, so the library cannot
    log in by itself.

    Intradel cookies stored in the session's cookie jar are cleared before the request.
    """
    cookie = _normalize_cookie(cookie)
    if not cookie:
        raise AuthenticationError("No cookie found in the provided value")

    _LOGGER.info("Will query data using a session cookie")
    # Intradel sets an anonymous PHPSESSID on any request without a session, and aiohttp lets
    # jar cookies override a hand-written Cookie header: a shared session would otherwise send
    # that anonymous session instead of ours. The header itself is sent exactly as pasted.
    session.cookie_jar.clear_domain(_COOKIE_DOMAIN)
    async with session.get(_DATA_URL, headers={"Cookie": cookie}, allow_redirects=False) as resp:
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


def _normalize_cookie(cookie: str) -> str:
    """Accept the cookie as copied from browser dev tools, e.g. "Cookie: PHPSESSID=...\\n"."""
    return _COOKIE_HEADER_PREFIX.sub("", cookie).strip()


__all__ = ["ApiError", "AuthenticationError", "IntradelError", "ParseError", "get_data"]
