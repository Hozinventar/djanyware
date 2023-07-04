# from mysite import settings
# from django.conf import settings
# settings.configure()
import requests
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

r = requests.post('http://127.0.0.1:8000/women/api/v1/auth/users/', json={'username': 'sdfsdf', 'password': 'sdfwefksjdnj'})  # создали польователя
r = requests.post('http://127.0.0.1:8000/auth/token/login/', json={'username': 'sdfsdf', 'password': 'sdfwefksjdnj'}) # получили токен

r = requests.get('http://127.0.0.1:8000/api/v1/womans/1/',
                 headers={'Content-Type': 'application/json', 'Authorization': 'Token 406b093071838e41b8362e83ce308b072afcc626'})

r = requests.post('http://127.0.0.1:8000/auth/token/login/', json={'username': 'admin', 'password': 'admin'}) # получили токен
r = requests.get('http://127.0.0.1:8000/api/v1/womans/1/',
                 headers={'Content-Type': 'application/json', 'Authorization': 'Token ecc070888d8a0d1ef6549903c86382e87f49cfa4'})