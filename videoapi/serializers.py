from rest_framework import serializers
from .models import Video
from . import validators


class UploadVideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(validators=[validators.validate_file_is_video])
    class Meta:
        model = Video
        fields = ['video']