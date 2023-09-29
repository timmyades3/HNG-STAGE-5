from django.urls import path
from . import views


urlpatterns=[
    path('',views.UploadVideo.as_view(), name='upload')
]