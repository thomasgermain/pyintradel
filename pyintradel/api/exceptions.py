class AuthenticationError(ValueError):
    """Intradel returned its login page instead of the requested data.

    Subclasses ValueError so callers catching the previous generic error keep working.
    """
