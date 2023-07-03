# from mysite import settings
# from django.conf import settings
# settings.configure()
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
from urllib3 import disable_warnings
disable_warnings()
import django
django.setup()

from django.contrib.auth.models import User
from woman.models import *
# myuser, created = Human.objects.get_or_create(name="Аркадий2", defaults={'age': 12, 'work': Work(name="Foo Bar")})

a = Woman.objects.all()
a1 = Woman.objects.get(pk=1)
u = User.objects.all().values()

print()



