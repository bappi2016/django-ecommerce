# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task, shared_task

from celery.utils.log import get_task_logger
from django.core.mail import send_mail

logger=get_task_logger(__name__)

#This is the decorator which a celery worker uses
@task
@shared_task(name="send_feedback_email_task")
def send_feedback_email_task(ref_code,email,message):
    logger.info("Sent email")
    return send_mail(''+ message +'And my reference code is' + ref_code,email,['ajmalhussainbappi@gmail.com'],fail_silently=False)



