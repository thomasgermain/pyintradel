import unittest
from typing import Any

from pyintradel import api
from tests.mock import CORRECT_RESPONSE


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
        self.post_calls: list[tuple[str, dict[str, str], dict[str, str]]] = []

    def get(self, url: str, headers: dict[str, str]) -> _FakeResponse:
        self.get_calls.append((url, headers))
        return self._response

    def post(self, url: str, data: dict[str, str], headers: dict[str, str]) -> _FakeResponse:
        self.post_calls.append((url, data, headers))
        return self._response


class GetDataTest(unittest.IsolatedAsyncioTestCase):
    async def test_missing_credentials_and_cookie_raises(self) -> None:
        session = _FakeSession(_FakeResponse(200, CORRECT_RESPONSE))
        with self.assertRaises(ValueError):
            await api.get_data(session)  # type: ignore[arg-type]

    async def test_cookie_uses_get_and_skips_login(self) -> None:
        session = _FakeSession(_FakeResponse(200, CORRECT_RESPONSE))
        result = await api.get_data(session, cookie="PHPSESSID=abc")  # type: ignore[arg-type]

        self.assertEqual(len(result), 3)
        self.assertEqual(len(session.get_calls), 1)
        self.assertEqual(len(session.post_calls), 0)
        _, headers = session.get_calls[0]
        self.assertEqual(headers["Cookie"], "PHPSESSID=abc")

    async def test_login_uses_post(self) -> None:
        session = _FakeSession(_FakeResponse(200, CORRECT_RESPONSE))
        result = await api.get_data(session, "user", "pass", "LIEGE")  # type: ignore[arg-type]

        self.assertEqual(len(result), 3)
        self.assertEqual(len(session.post_calls), 1)
        self.assertEqual(len(session.get_calls), 0)
