#  когда нужны вспомогательные классы
from .models import *
from django.db.models import *
from django.core.cache import cache

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    ]


class DataMixin:
    def get_user_context(self, **kwargs):
        """ дополняет контекст , что формируется автоматически и дополняет нуными атрибутами для шаблона """
        context = kwargs
        # ниже пример авторизации и чтобы не отображать нужное поле меню
        m = menu[:]
        if not self.request.user.is_authenticated:
            m.pop(1)
            # breakpoint()
        context['menu'] = m
        # context['categ'] = Category.objects.all()

        categ = cache.get('categ')
        # if (categ := cache.get('categ')) is not None:
        if not categ:
            categ = Category.objects.annotate(total=Count('woman')).filter(total__gt=0)  # annotate значит ленивый запрос.
            print(categ)
            cache.set('categ', categ, 60)  # 60 секунд

        context['categ'] = categ
        # отображать только те категории где есть записи. больше 0 т.е. если пусто то не покажется в сайтбаре
        if 'selected' not in context:
            context['selected'] = 0
        return context
