from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


def custom_exception_handler(exc, context):
    # Letting DRF handle it first
    response = exception_handler(exc, context)

    # If DRF handled it, standardizing the format
    if response is not None:
        custom_response = {
            "status_code": response.status_code,
            "error": _get_error_message(exc),
            "detail": response.data
        }
        return Response(custom_response, status=response.status_code)

    # If DRF didn't handle it, handling known Django errors or fallback
    if isinstance(exc, DjangoValidationError):
        return Response({
            "status_code": status.HTTP_400_BAD_REQUEST,
            "error": "Validation Error",
            "detail": exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
        }, status=status.HTTP_400_BAD_REQUEST)

    # Unknown unhandled errors (e.g., 500s)
    return Response({
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "error": "Internal Server Error",
        "detail": str(exc)
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_error_message(exc):
    """Convert exception class names to human-readable error types."""
    if isinstance(exc, DRFValidationError):
        return "Validation Error"
    from rest_framework.exceptions import NotFound, PermissionDenied, AuthenticationFailed
    if isinstance(exc, NotFound):
        return "Not Found"
    if isinstance(exc, PermissionDenied):
        return "Permission Denied"
    if isinstance(exc, AuthenticationFailed):
        return "Authentication Failed"
    return exc.__class__.__name__
