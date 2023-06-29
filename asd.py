# from mysite import settings
# from django.conf import settings
# settings.configure()
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
from urllib3 import disable_warnings
disable_warnings()
import django
django.setup()

from woman.models import *
# myuser, created = Human.objects.get_or_create(name="Аркадий2", defaults={'age': 12, 'work': Work(name="Foo Bar")})
print()



