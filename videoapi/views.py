import base64
from io import BytesIO
import os
import subprocess
from django.conf import settings
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
from deepgram import Deepgram
from decouple import config
import mimetypes

import asyncio

import boto3



# Create your views here.

class UploadVideo(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = UploadVideoSerializer

    async def transcribe_audio(self, unique_name):
            deepgram = Deepgram("2930598b2500b43928ae66bbaf437a843b8c48a4")
            audio = open(unique_name, 'rb')
            source = {
            'buffer': audio,
            'mimetype': 'audio/mp3'
            }

            # Send the audio to Deepgram and get the response
            response = await asyncio.create_task(
                deepgram.transcription.prerecorded(
                source,
                {
                    'smart_format': True,
                    'model': 'nova',
                }
                )
            )
            result = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            return result
    def post(self, request, *args, **kwargs):
        serializer = UploadVideoSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            # ... (other validation and processing code)

            # Save the video to AWS S3 bucket
            video = serializer.validated_data.get('video')
            video_name = video.name
            s3_key = f'media/videos/{video_name}'  # Modify the S3 key as per your configuration
            s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': s3_key
                },
                ExpiresIn=3600000
            )
                          
            with NamedTemporaryFile(delete=False) as temp_file:
                for chunk in video.chunks():
                    temp_file.write(chunk)
            
        
            unique_id = str(uuid.uuid4())[:8]
            name,ext = os.path.splitext(video_name)
            unique_name = f'{name}_{unique_id}.mp3'
            
            subprocess.run(f'ffmpeg -i "{temp_file.name}" "{unique_name}"',shell=True)

            # Call the async function to transcribe audio
            transcription_result = asyncio.run(self.transcribe_audio(unique_name))
            serializer.save(transcription = transcription_result)
            # Return the S3 URL for the video and the transcription in the response
            os.remove(unique_name)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class UploadVideo(generics.CreateAPIView):
#     queryset = Video.objects.all()
#     # parser_classes = (MultiPartParser, FormParser)
#     serializer_class = UploadVideoSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = UploadVideoSerializer(
#             data=request.data, context={"request": request}
#         )
        
#         if serializer.is_valid():
#             # title = serializer.validated_data.get('title')
#             # base64_video = serializer.validated_data.get('base64_video')
#             # video_data = base64.b64decode(base64_video)
#             # print (video_data)
#             # f = ContentFile(video_data)
#             # video = Video(title=title)
#             # video.video.save(f'{title}.mp4', f, save=True)
#             # video.save()
            
#             # position_35_character = base64_video[43]
#             # print(position_35_character)
#             # data = ContentFile(base64.b64decode(base64_video), name=f'{title}.mp4')
#             # videoinstance = Video.objects.create(title=title,video=data)
#             # # videoinstance.video.save(f'{title}.mp4', ContentFile(base64.b64decode(base64_video)), save=True)
#             # print(data)
#             # video_np_array = np.frombuffer(video_data, dtype=np.uint8)
#             # model =whisper.load_model("base")
#             # option = whisper.DecodingOptions(fp16=False)
#             # result = model.transcribe(video_np_array)
#             # final_result = f'{result["text"]}'
#             # `videoinstance.save()
#             # response = {
#             #     "video":video.video
#             # }

#             video = serializer.validated_data.get('video')
#             print(video)
#             video_name = video.name
            
#             with NamedTemporaryFile(delete=False) as temp_file:
#                 for chunk in video.chunks():
#                     temp_file.write(chunk)
            
#             # video_clip = VideoFileClip(temp_file.name)
#             # audio_clip = video_clip.audio
#             unique_id = str(uuid.uuid4())[:8]
#             name,ext = os.path.splitext(video_name)
#             unique_name = f'{name}_{unique_id}.wav'
#             # audio_clip.write_audiofile( f'{unique_name}', codec='pcm_s16le')
            
#             subprocess.run(f'ffmpeg -i "{temp_file.name}" "{unique_name}"',shell=True)
            
            
#             # r = sr.Recognizer()
            
#             # # Load the audio file
#             # with sr.AudioFile(unique_name) as source:
#             #     data = r.record(source)
            
#             # # Convert speech to text
#             # text = r.recognize_google(data)
                        
           
#             async def transcribe_audio():
#                 dg_client = Deepgram(config('Deepgram_api_key'))   
#                 with open(unique_name, 'rb') as audio:
#                     source = {'buffer': audio, 'mimetype': 'audio/mp3' }
#                 response = await dg_client.transcription.prerecorded(source, {'punctuate': True})
#                 result = response['results']['channels'][0]['alternatives'][0]['transcript']
#                 serializer.save(transcription= result)
                        
#                 return Response(serializer.data, status=status.HTTP_200_OK)
                
                
#             transcribe_audio()
           
            
#             # model =whisper.load_model("tiny", device="cpu")
#             # option = whisper.DecodingOptions(fp16=False)
#             # result = model.transcribe(temp_file.name)
#             # final_result = f'{result["text"]}'
#             # print(video_name)
            
#             # transcribe_video.delay(video_obj.id)
           
            
#             # return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

