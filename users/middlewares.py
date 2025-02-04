from django.http import HttpRequest

from .models import User
from .services import verify_jwt

class AuthMiddleware():
    """ Authorization middleware """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        request.authorized = False

        access_token = request.COOKIES.get('access_token', None)

        if isinstance(access_token, str) and len(access_token) > 0:
            try:
                token_payload = verify_jwt(access_token)
                user = User.objects.get(pk=token_payload.get('id'))
            except Exception:
                user = None

            request.user_info = user
            request.authorized = user is not None

        response = self.get_response(request)
        return response
