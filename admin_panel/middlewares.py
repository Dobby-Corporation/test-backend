import re
from django.http import HttpRequest, HttpResponse

class LoginMiddleware():
    """ Authorization middleware """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        is_active = re.match('^\/panel(\/.*)?', request.path) is not None
        
        if is_active and not request.user.is_superuser:
            return HttpResponse(status=403)
        response = self.get_response(request)
        return response
