from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def page_not_found(request: HttpRequest, exception=None) -> HttpResponse:
    """
    Custom 404 error handler.

    Args:
        request (HttpRequest): The HTTP request object.
        exception: The exception that triggered the 404 error.

    Returns:
        HttpResponse: Response with a 404 status code and a custom error message.
    """
    return HttpResponse('Error handler content', status=404)

def csrf_failure(request: HttpRequest, reason: str='') -> HttpResponse:
    """
    Custom CSRF failure handler.

    Args:
        request (HttpRequest): The HTTP request object.
        reason (str): The reason for CSRF failure.

    Returns:
        HttpResponse: Rendered response with a 403 status code and a custom template for CSRF failure.
    """
    return render(request, 'core/403csrf.html', context={'reason': reason}, status=403)

def server_error(request: HttpRequest) -> HttpResponse:
    """
    Custom 500 error handler.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered response with a 500 status code and a custom error template.
    """
    return render(request, 'core/500.html', status=500)
