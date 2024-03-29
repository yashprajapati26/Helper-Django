"""
Celery config file

https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html

"""
from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helper_project.settings')

# you change change the name here
app = Celery("helper_project")

app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata' )

# read config from Django settings, the CELERY namespace would make celery 
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')


from celery.schedules import crontab
# Celery Beat Settings
app.conf.beat_schedule = {

    'send_mail_everyday' : {
        'task' : 'helper_app.utils.send_mail_by_admin',
        'schedule' : crontab(hour=19,minute=10),
    }
} 



# load tasks.py in django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


