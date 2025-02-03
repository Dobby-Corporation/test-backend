from django.template import loader
from django.http import HttpRequest, HttpResponse

# Create your views here.
def index(request: HttpRequest):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
