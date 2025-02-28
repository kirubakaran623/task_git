from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newproject.settings')

app = Celery('newproject')

# Read config from Django settings, the CELERY_ namespace means
# all CELERY_* keys in settings.py get passed into Celery automatically.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Use django-celery-beat scheduler

