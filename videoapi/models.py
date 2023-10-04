from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=1000, default='untitled_video' )
    video = models.FileField(upload_to="videos")
    transcription = models.TextField(null=True)

    def __str__(self):
        return f'{self.video.name}'
    