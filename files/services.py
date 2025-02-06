import uuid

from django.core.files.base import ContentFile
from .models import File

def create_file_from_str(content: str) -> File:
    file = File(name='', file=None, type='', uuid=uuid.uuid4())
    file.file.save('a.py', ContentFile(content, ''))
    file.save()
    return file

def get_file_by_uuid(uuid: str) -> File:
    return File.objects.get(uuid=uuid)

def is_valid_uuid(uuidval: str) -> bool:
    try:
        uuid.UUID(str(uuidval))
        return True
    except ValueError:
        return False
