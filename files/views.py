from django.http import FileResponse, HttpResponse

from . import services

# Create your views here.
def get_file(_request, file_uuid):
    if not services.is_valid_uuid(file_uuid):
        return HttpResponse(status=400)

    file = services.get_file_by_uuid(file_uuid)
    return FileResponse(file.file)
