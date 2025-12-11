from fastapi import HTTPException, status

class AppException(HTTPException):
    """
    Base application exception with clean formatting.
    """

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail={"error": message})


class NotFoundException(AppException):
    def __init__(self, message="Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class UnauthorizedException(AppException):
    def __init__(self, message="Unauthorized access"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    def __init__(self, message="Access denied"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class ValidationException(AppException):
    def __init__(self, message="Validation error"):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)
