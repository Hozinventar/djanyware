import os
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
import django
django.setup()

# таска без ретерна
from mysite.celery import debug_task
debug_task.delay()

# таска с ретерном
from woman.tasks import bar
bar.delay()

print('d')