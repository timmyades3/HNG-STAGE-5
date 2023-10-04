from rest_framework import serializers
from .models import Video
from . import validators


class UploadVideoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(validators=[validators.validate_file_is_video],required=False)
    base64_video = serializers.CharField(
        validators=[validators.validate_base64],
        required=False
        )
    title = serializers.CharField( write_only = True,required=False)
    # video_array = serializers.ListField(child=serializers.CharField(use_url=False, write_only = True))
    # video_url = serializers.SerializerMethodField(read_only=True) 
    transcription = serializers.CharField(read_only=True)
    class Meta:
        model = Video
        fields = ['pk',
                  'video',
                  # 'video_url',
                  # 'video_array',
                  'title',
                  'base64_video',
                  'transcription']

    # def get_video_url(self, obj):
    #     request = self.context.get('request')
    #     if obj.video:
    #         return request.build_absolute_uri(obj.video.url)
    #     return None