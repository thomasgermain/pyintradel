class IntradelError(ValueError):
    """Base class for all errors raised by this library.

    Subclasses ValueError so callers catching the previous generic error keep working.
    """


class AuthenticationError(IntradelError):
    """Intradel refused the session cookie and sent its login page instead of the data."""

    def __init__(
        self,
        message: str = "Session cookie rejected by intradel, it is probably expired or invalid",
    ) -> None:
        super().__init__(message)


class ApiError(IntradelError):
    """Intradel answered with an unexpected HTTP status."""

    def __init__(self, status: int) -> None:
        # args must hold the constructor input, so copy/pickle rebuild the same error.
        super().__init__(status)
        self.status = status

    def __str__(self) -> str:
        return f"HTTP {self.status} from intradel"


class ParseError(IntradelError):
    """The page does not have the expected structure, likely after a website change."""
