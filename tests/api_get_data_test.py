import pickle
import unittest
from typing import Any

from pyintradel import api
from tests.mock import CORRECT_RESPONSE, INCORRECT_LOGIN


class _FakeResponse:
    def __init__(self, status: int, body: str | bytes) -> None:
        self.status = status
        self._body = body.encode() if isinstance(body, str) else body

    async def text(self, errors: str = "strict") -> str:
        return self._body.decode("utf-8", errors)

    async def __aenter__(self) -> "_FakeResponse":
        return self

    async def __aexit__(self, *exc: Any) -> bool:
        return False


class _FakeSession:
    def __init__(self, response: _FakeResponse) -> None:
        self._response = response
        self.get_calls: list[tuple[str, dict[str, str]]] = []
        self.allow_redirects: list[bool] = []

    def get(self, url: str, headers: dict[str, str], allow_redirects: bool) -> _FakeResponse:
        self.get_calls.append((url, headers))
        self.allow_redirects.append(allow_redirects)
        return self._response


class GetDataTest(unittest.IsolatedAsyncioTestCase):
    async def test_cookie_is_sent_as_header(self) -> None:
        session = _FakeSession(_FakeResponse(200, CORRECT_RESPONSE))
        result = await api.get_data(session, "PHPSESSID=abc")  # type: ignore[arg-type]

        self.assertEqual(len(result), 3)
        self.assertEqual(len(session.get_calls), 1)
        _, headers = session.get_calls[0]
        self.assertEqual(headers["Cookie"], "PHPSESSID=abc")

    async def test_redirect_to_login_raises_authentication_error(self) -> None:
        session = _FakeSession(_FakeResponse(302, ""))
        with self.assertRaisesRegex(api.AuthenticationError, "cookie"):
            await api.get_data(session, "PHPSESSID=expired")  # type: ignore[arg-type]

        # Following the redirect would download and parse the whole login page.
        self.assertEqual(session.allow_redirects, [False])

    async def test_login_page_served_directly_raises_authentication_error(self) -> None:
        session = _FakeSession(_FakeResponse(200, INCORRECT_LOGIN))
        with self.assertRaisesRegex(api.AuthenticationError, "cookie"):
            await api.get_data(session, "PHPSESSID=expired")  # type: ignore[arg-type]

    async def test_http_error_raises_api_error_without_body(self) -> None:
        session = _FakeSession(_FakeResponse(503, "<html>" + "x" * 10_000 + "</html>"))
        with self.assertRaises(api.ApiError) as ctx:
            await api.get_data(session, "PHPSESSID=abc")  # type: ignore[arg-type]

        self.assertEqual(ctx.exception.status, 503)
        self.assertEqual(str(ctx.exception), "HTTP 503 from intradel")

    async def test_undecodable_error_body_still_raises_api_error(self) -> None:
        session = _FakeSession(_FakeResponse(502, b"\xff\xfe not utf-8"))
        with self.assertLogs("pyintradel.api", "DEBUG"), self.assertRaises(api.ApiError):
            await api.get_data(session, "PHPSESSID=abc")  # type: ignore[arg-type]

    def test_api_error_survives_pickle(self) -> None:
        err = pickle.loads(pickle.dumps(api.ApiError(503)))

        self.assertEqual(err.status, 503)
        self.assertEqual(str(err), "HTTP 503 from intradel")

    async def test_cookie_copied_from_dev_tools_is_normalized(self) -> None:
        for raw in ("Cookie: PHPSESSID=abc", "cookie:PHPSESSID=abc\n", "  PHPSESSID=abc \r\n"):
            session = _FakeSession(_FakeResponse(200, CORRECT_RESPONSE))
            await api.get_data(session, raw)  # type: ignore[arg-type]

            _, headers = session.get_calls[0]
            self.assertEqual(headers["Cookie"], "PHPSESSID=abc", raw)
