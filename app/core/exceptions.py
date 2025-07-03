class AppException(Exception):
    """Base class for application exceptions."""


class ServerRegistrationError(AppException):
    """Raised when server registration fails."""


class ServerNotFoundError(AppException):
    """Raised when a requested server is not found."""


class QueryProcessingError(AppException):
    """Raised when a query cannot be processed."""

