class IntradelError(ValueError):
    """Base class for all errors raised by this library.

    Subclasses ValueError so callers catching the previous generic error keep working.
    """


class AuthenticationError(IntradelError):
    """Intradel returned its login page instead of the requested data."""


class ApiError(IntradelError):
    """Intradel answered with an unexpected HTTP status."""

    def __init__(self, status: int) -> None:
        super().__init__(f"HTTP {status} from intradel")
        self.status = status


class ParseError(IntradelError):
    """The page does not have the expected structure, likely after a website change."""
