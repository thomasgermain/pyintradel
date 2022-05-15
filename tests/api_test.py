import unittest

from pyintradel.parser import parse
from tests.mock import CORRECT_RESPONSE, INCORRECT_LOGIN


class ParsingTest(unittest.TestCase):
    def test_parsing_correct(self) -> None:
        result = parse(CORRECT_RESPONSE)
        self.assertEqual(len(result), 3)

    def test_parsing_login_error(self) -> None:
        self.assertRaises(ValueError, parse, INCORRECT_LOGIN)
