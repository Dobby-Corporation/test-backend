from django.template import loader
from django.http import HttpRequest, HttpResponse

# Create your views here.
def index(_request: HttpRequest):
    """ Main page """
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
