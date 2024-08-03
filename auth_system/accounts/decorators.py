
from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .utils import is_blocked

def check_ip_block(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        ip_address = request.META.get('REMOTE_ADDR')
        if is_blocked(ip_address):
            return Response({'error': 'Your IP is blocked. Please try again later.'}, status=status.HTTP_403_FORBIDDEN)
        return view_func(self, request, *args, **kwargs)
    return _wrapped_view
