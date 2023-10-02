import base64
from io import BytesIO
import os
from django.shortcuts import render
import numpy as np
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# from .tasks import transcribe_video
from .models import Video
from .serializers import UploadVideoSerializer
from tempfile import NamedTemporaryFile, TemporaryFile
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files import File
import whisper
import imageio
import uuid


# Create your views here.


class UploadVideo(generics.CreateAPIView):
    queryset = Video.objects.all()
    # parser_classes = (MultiPartParser, FormParser)
    serializer_class = UploadVideoSerializer

    def post(self, request, *args, **kwargs):
        serializer = UploadVideoSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            # title = serializer.validated_data.get('title')
            # base64_video = serializer.validated_data.get('base64_video')
            # video_data = base64.b64decode(base64_video)
            # print (video_data)
            # f = ContentFile(video_data)
            # video = Video(title=title)
            # video.video.save(f'{title}.mp4', f, save=True)
            # video.save()
            
            # position_35_character = base64_video[43]
            # print(position_35_character)
            # data = ContentFile(base64.b64decode(base64_video), name=f'{title}.mp4')
            # videoinstance = Video.objects.create(title=title,video=data)
            # # videoinstance.video.save(f'{title}.mp4', ContentFile(base64.b64decode(base64_video)), save=True)
            # print(data)
            # video_np_array = np.frombuffer(video_data, dtype=np.uint8)
            # model =whisper.load_model("base")
            # option = whisper.DecodingOptions(fp16=False)
            # result = model.transcribe(video_np_array)
            # final_result = f'{result["text"]}'
            # `videoinstance.save()
            # response = {
            #     "video":video.video
            # }

            video = serializer.validated_data.get('video')
            print(video)
            video_name = video.name
            with NamedTemporaryFile(delete=False) as temp_file:
                for chunk in video.chunks():
                    temp_file.write(chunk)
            model =whisper.load_model("tiny", device="cpu")
            option = whisper.DecodingOptions(fp16=False)
            result = model.transcribe(temp_file.name)
            final_result = f'{result["text"]}'
            print(video_name)
            serializer.save(transcription = final_result)
            # transcribe_video.delay(video_obj.id)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

