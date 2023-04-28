import os
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
import django
django.setup()
from woman.tasks import add

add.delay(1, 2)


