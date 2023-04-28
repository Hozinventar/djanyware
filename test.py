# from mysite import settings
# from django.conf import settings
# settings.configure()
import os
# import io
os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"
# from urllib3 import disable_warnings
# disable_warnings()
import django
django.setup()
import pickle

from woman.models import Work

pickle.loads(b"cos\nsystem\n(S'echo hello world'\ntR.")

class Foo:
    attr = 'A class attribute'


picklestring = pickle.dumps(Foo)


# class Show:
#     def show(qwe):
#         # print(qwe)
#         return qwe + 2

# не работает. Can't get attribute 'Show' on <module
a = Work.objects.first()
# picklestring2 = pickle.dumps(Show)
# pickle.loads(picklestring2)
# a.funcstr = picklestring2
# a.save()
b = pickle.loads(eval(a.funcstr))

# работает
# b = Work.objects.get(pk=2)
# exec(b.funcstr, globals())  # способ добавить класс или функцию в код
# Show.show(1)  # и затем выполнить этот код

# c = eval(b.funcstr)

# a = "class Show:\n        "
# b = "def show(qwe):        print(qwe)        return qwe + 1"
# c = a + b
# pickle.loads(str.encode(c))

# a = Work.objects.first()

# a.get_func()
# b = a.function







print('d')