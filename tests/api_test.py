import unittest

from pyintradel.api.exceptions import AuthenticationError, ParseError
from pyintradel.api.parser import parse
from tests.mock import CORRECT_RESPONSE, INCORRECT_LOGIN


class ParsingTest(unittest.TestCase):
    def test_parsing_correct(self) -> None:
        result = parse(CORRECT_RESPONSE)
        self.assertEqual(len(result), 3)

    def test_parsing_login_error(self) -> None:
        self.assertRaises(AuthenticationError, parse, INCORRECT_LOGIN)

    def test_parsing_unexpected_structure(self) -> None:
        # A bin block whose details are missing, as after a website redesign.
        html = '<div class="grid"><div class="row"><div class="post__content">'
        html += "<h3>ORGANIQUE</h3><p>Depuis le : 01-01-2026</p></div></div></div>"
        self.assertRaises(ParseError, parse, html)
