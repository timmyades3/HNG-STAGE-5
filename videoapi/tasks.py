import os
from tempfile import NamedTemporaryFile
from celery import shared_task
from .models import Video
import whisper

@shared_task
def transcribe_video(video_id):
    try:
        videoid = Video.objects.get(id=video_id)
        video = videoid.video
        video_name = videoid.video.name

        with NamedTemporaryFile(delete=False) as temp_file:
            for chunk in video.chunks():
                temp_file.write(chunk)
        model = whisper.load_model("small")
        option = whisper.DecodingOptions(fp16=False)
        result = model.transcribe(temp_file.name)
        final_result = f'{result["text"]}'
        
        # Update the Video model with the transcription
        videoid.transcription = final_result
        videoid.save()
    except Video.DoesNotExist:
        pass  # Handle the case where the video doesn't exist

    return "Transcription complete"
