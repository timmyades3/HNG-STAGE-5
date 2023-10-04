import base64
import os
import subprocess
from django.conf import settings
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# from .tasks import transcribe_video
from .models import Video
from .serializers import UploadVideoSerializer
from tempfile import NamedTemporaryFile
from django.core.files.base import ContentFile
import uuid
from deepgram import Deepgram
from decouple import config
import asyncio
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_audio
import boto3
from rest_framework import serializers
from rest_framework.decorators import api_view

class UploadVideo(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = UploadVideoSerializer

    async def transcribe_audio(self, unique_name):
            deepgram = Deepgram(config('DEEPGRAM_APIKEY'))
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
            video = serializer.validated_data.get('video')
            base64_video = serializer.validated_data.get('base64_video')
            title = serializer.validated_data.get('title')

            if video:
                if title or base64_video:
                    raise serializers.ValidationError("Error: You cannot send 'title' or 'base64_video' along with 'video'.")

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
                
                mp3_tempfile = NamedTemporaryFile(delete=False, suffix=".mp3").name
                ffmpeg_extract_audio(temp_file.name, mp3_tempfile)
                        
                # Call the async function to transcribe audio
                transcription_result = asyncio.run(self.transcribe_audio(mp3_tempfile))
                serializer.save(transcription = transcription_result)
                # Return the S3 URL for the video and the transcription in the response
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif (title and base64_video):
                if (title and video) or (base64_video and video):
                    raise serializers.ValidationError("Error: You must send either 'video' or a combination of 'title' and 'base64_video'.")
                unique_id = str(uuid.uuid4())[:8]
                c_title = f'{title}_{unique_id}'
                video_data = base64.b64decode(base64_video)
                f = ContentFile(video_data)
                video = Video(title=c_title)
                video.video.save(f'{c_title}.mp4', f, save=True)
                
                
                s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME  
                s3_object_key = f'videos/{c_title}.mp4'  
                s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

                response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
                video_bytes = response['Body'].read()

                # Create a temporary file to save the video
                video_tempfile = NamedTemporaryFile(delete=False, suffix=".mp4")
                with open(video_tempfile.name, 'wb') as video_file:
                    video_file.write(video_bytes)

                # Extract audio from video using ffmpeg_extract_audio
                mp3_tempfile = NamedTemporaryFile(delete=False, suffix=".mp3").name
                ffmpeg_extract_audio(video_tempfile.name, mp3_tempfile)
                        
                transcription_result = asyncio.run(self.transcribe_audio(mp3_tempfile))
                video.transcription = transcription_result
                video.save()
                
                response = {
                    "pk":video.pk,
                    "video":video.video.url,
                    "transcription":video.transcription
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def TranscriptionRetrieveApiview(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            try:
                
                obj = get_object_or_404(Video,pk=pk)
                data = UploadVideoSerializer(obj, many=False).data
                data = {"transcription": obj.transcription} 
                return Response(data)
            except Video.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def videoRetrieveApiview(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            try:
                
                obj = get_object_or_404(Video,pk=pk)
                data = UploadVideoSerializer(obj, many=False).data
                data = {"video": obj.video.url} 
                return Response(data)
            except Video.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)



# class UploadVideo(generics.CreateAPIView):
#     queryset = Video.objects.all()
#     # parser_classes = (MultiPartParser, FormParser)
#     serializer_class = UploadVideoSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = UploadVideoSerializer(
#             data=request.data, context={"request": request}
#         )
        
#         if serializer.is_valid():
#             title = serializer.validated_data.get('title')
#             unique_id = str(uuid.uuid4())[:8]
#             c_title = f'{title}_{unique_id}'
#             base64_video = serializer.validated_data.get('base64_video')
#             video_data = base64.b64decode(base64_video)
#             f = ContentFile(video_data)
#             video = Video(title=c_title)
#             video.video.save(f'{title}.mp4', f, save=True)
#             video.save()
            
#             s3_bucket_name = settings.AWS_STORAGE_BUCKET_NAME  
#             s3_object_key = f'videos/{title}.mp4'  
#             s3_client = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

#             response = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_object_key)
#             video_bytes = response['Body'].read()

#             # Create a temporary file to save the video
#             video_tempfile = NamedTemporaryFile(delete=False, suffix=".mp4")
#             with open(video_tempfile.name, 'wb') as video_file:
#                 video_file.write(video_bytes)

#             # Extract audio from video using ffmpeg_extract_audio
#             mp3_tempfile = NamedTemporaryFile(delete=False, suffix=".mp3").name
#             ffmpeg_extract_audio(video_tempfile.name, mp3_tempfile)
                     
#             model =whisper.load_model("base")
#             option = whisper.DecodingOptions(fp16=False)
#             result = model.transcribe(mp3_tempfile)
#             final_result = f'{result["text"]}'
        
#             response = {
#                 "video":video.video.url,
#                 "transcription":final_result
#             }

#             # video = serializer.validated_data.get('video')
#             # print(video)
#             # video_name = video.name
            
#             # with NamedTemporaryFile(delete=False) as temp_file:
#             #     for chunk in video.chunks():
#             #         temp_file.write(chunk)
            
#             # # video_clip = VideoFileClip(temp_file.name)
#             # # audio_clip = video_clip.audio
#             # unique_id = str(uuid.uuid4())[:8]
#             # name,ext = os.path.splitext(video_name)
#             # unique_name = f'{name}_{unique_id}.wav'
#             # # audio_clip.write_audiofile( f'{unique_name}', codec='pcm_s16le')
            
#             # subprocess.run(f'ffmpeg -i "{temp_file.name}" "{unique_name}"',shell=True)
            
#             # model =whisper.load_model("tiny", device="cpu")
#             # option = whisper.DecodingOptions(fp16=False)
#             # result = model.transcribe(temp_file.name)
#             # final_result = f'{result["text"]}'
#             # print(video_name)
            
#             # transcribe_video.delay(video_obj.id)
           
            
#             return Response(response, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

