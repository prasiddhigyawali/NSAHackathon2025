from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os

# Create your models here.

class AudioRecording(models.Model):
    title = models.CharField(max_length=100, blank=True)
    audio_file = models.FileField(upload_to="recordings/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or f"Recording {self.id}"
    
    class Meta:
        db_table = 'audio_recording'  # Explicit table name
    

#     from django.db import models
