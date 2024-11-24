from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotFound, NotAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError):
        logger.error(f"Unhandled error: {exc}")
        custom_response_data = {
            "error": "ValidationError",
            "details": "Validation Error",
        }
        return Response(custom_response_data, status=response.status_code)

    if isinstance(exc, NotAuthenticated):
        logger.error(f"Unhandled error: {exc}")
        custom_response_data = {
            "error": "NotAuthenticated",
            "details": "Not Authenticated",
        }
        return Response(custom_response_data, status=response.status_code)

    if isinstance(exc, AuthenticationFailed):
        logger.error(f"Unhandled error: {exc}")
        custom_response_data = {
            "error": "AuthenticationFailed",
            "details": "Authentication Failed",
        }
        return Response(custom_response_data, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, PermissionDenied):
        logger.error(f"Unhandled error: {exc}")
        custom_response_data = {
            "error": "PermissionDenied",
            "details": "Permission Denied",
        }
        return Response(custom_response_data, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, NotFound):
        logger.error(f"Unhandled error: {exc}")
        custom_response_data = {
            "error": "NotFound",
            "details": "Not Found",
        }
        return Response(custom_response_data, status=status.HTTP_404_NOT_FOUND)

    return response
