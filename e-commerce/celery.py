# celery.py 

from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings




# set the default Django setting module for the celery program
os.environ.setdefault('DJANGO_SETTING_MODULE','e-commerce.settings.development')



app=Celery('e-commerce')
# app = Celery('e-commerce',broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


 


