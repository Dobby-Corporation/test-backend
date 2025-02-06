import uuid

from django.core.files.base import ContentFile
from .models import File

def create_file_from_str(content: str, name='unknown', type='') -> File:
    file = File(uuid=uuid.uuid4(), name=name, file=None, type=type)
    file.file.save(name, ContentFile(content, name))
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
