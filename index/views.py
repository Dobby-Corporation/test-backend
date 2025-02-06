from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def index(request: HttpRequest):
    """ Main page """
    return render(request, 'index.html')
