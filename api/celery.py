import os
from celery import Celery

# change myproject with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
app = Celery("api")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')