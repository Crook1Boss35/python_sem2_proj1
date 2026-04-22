class AppError(Exception):
    """Base application error."""


class ConflictError(AppError):
    """Raised when a resource already exists or conflicts with current state."""


class UnauthorizedError(AppError):
    """Raised when authentication fails."""


class ForbiddenError(AppError):
    """Raised when access is forbidden."""


class NotFoundError(AppError):
    """Raised when a resource is not found."""


class ExternalServiceError(AppError):
    """Raised when an external service returns an error."""
