import unittest
from typing import Any

from pyintradel import api
from tests.mock import CORRECT_RESPONSE, INCORRECT_LOGIN


class _FakeResponse:
    def __init__(self, status: int, text: str) -> None:
        self.status = status
        self._text = text

    async def text(self) -> str:
        return self._text

    async def __aenter__(self) -> "_FakeResponse":
        return self

    async def __aexit__(self, *exc: Any) -> bool:
        return False


class _FakeSession:
    def __init__(self, response: _FakeResponse) -> None:
        self._response = response
        self.get_calls: list[tuple[str, dict[str, str]]] = []

    def get(self, url: str, headers: dict[str, str]) -> _FakeResponse:
        self.get_calls.append((url, headers))
        return self._response


class GetDataTest(unittest.IsolatedAsyncioTestCase):
    async def test_cookie_is_sent_as_header(self) -> None:
        session = _FakeSession(_FakeResponse(200, CORRECT_RESPONSE))
        result = await api.get_data(session, "PHPSESSID=abc")  # type: ignore[arg-type]

        self.assertEqual(len(result), 3)
        self.assertEqual(len(session.get_calls), 1)
        _, headers = session.get_calls[0]
        self.assertEqual(headers["Cookie"], "PHPSESSID=abc")

    async def test_rejected_cookie_raises_authentication_error(self) -> None:
        session = _FakeSession(_FakeResponse(200, INCORRECT_LOGIN))
        with self.assertRaisesRegex(api.AuthenticationError, "cookie"):
            await api.get_data(session, "PHPSESSID=expired")  # type: ignore[arg-type]
