import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class File(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=63)
    file = models.FileField(upload_to=settings.MEDIA_ROOT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
