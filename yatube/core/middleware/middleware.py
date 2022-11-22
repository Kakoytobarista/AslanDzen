from django.core.exceptions import PermissionDenied


class FilterIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        blocked_ips = ['141.255.166.2',
                       '195.154.211.56', ]
        ip = request.META.get('REMOTE_ADDR')
        if ip in blocked_ips:
            raise PermissionDenied

        response = self.get_response(request)

        return response
