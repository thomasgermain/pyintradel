from pathlib import Path

_FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> str:
    # Decode bytes rather than read_text() so the \r\n in the scraped pages are kept verbatim.
    return (_FIXTURES / name).read_bytes().decode("utf-8")


CORRECT_RESPONSE = _load("correct_response.html")
INCORRECT_LOGIN = _load("incorrect_login.html")
