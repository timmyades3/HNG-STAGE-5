import binascii
from rest_framework import serializers
import os

def validate_base64(value):
    try:
        import base64
        # Attempt to decode the input value as Base64
        base64.b64decode(value)
    except (binascii.Error, TypeError):
        raise serializers.ValidationError("Invalid Base64 format")
    
def validate_file_is_video(value):
    format = os.path.splitext(value.name)[1]
    format = format.lower()
    allowed_format = ['.mp4','.mkv','.mov','.wmv','.avi','.flv','.webm','.avchd']
    if not format in allowed_format:
        raise serializers.ValidationError(f'File format is not supported')
    return value
