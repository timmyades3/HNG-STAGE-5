from django.urls import path
from . import views


urlpatterns=[
    path('',views.UploadVideo.as_view(), name='upload'),
    path('api/transcription/<int:pk>/',views.TranscriptionRetrieveApiview , name='transcrition_detail'),
    path('api/video/<int:pk>/',views.videoRetrieveApiview, name='video_detail'),
]