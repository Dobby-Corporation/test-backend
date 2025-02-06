from django.shortcuts import HttpResponse

def login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.authorized:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(status=403)
    return wrapper_func
