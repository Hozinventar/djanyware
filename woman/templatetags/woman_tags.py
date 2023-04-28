from django import template
from woman.models import *

register = template.Library()


# @register.simple_tag(name='cats')  # переопределяем имя функции. и в шаблоне jinja можно импортировать уже по этому имени
# @register.simple_tag(name="catego")
# def get_categories():
#     return Category.objects.all()


@register.simple_tag()
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)


@register.inclusion_tag('woman/show_posts.html')
def get_posts(filter=None):
    if not filter:
        posts = Woman.objects.all()
    else:
        posts = Woman.objects.filter(cat_id=filter)
    return {"posts": posts}


@register.inclusion_tag('woman/list_cats.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'categ': cats, "selected": cat_selected}
