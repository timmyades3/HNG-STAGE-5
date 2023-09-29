from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Video
from.serializers import UploadVideoSerializer


# Create your views here.


class UploadVideo(generics.CreateAPIView):
    queryset=Video.objects.all()
    serializer_class= UploadVideoSerializer

    def post(self, request, *args, **kwargs):
        serializer = UploadVideoSerializer(data = request.data)
        if serializer.is_valid():
            # video = serializer.validated_data.get('video')
            video  =  request.FILES.get('video')
            video_name = video.name
            print(video_name)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)