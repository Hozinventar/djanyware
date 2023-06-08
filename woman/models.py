from django.db import models
from django.urls import reverse
import pickle
import codecs
from rest_framework import serializers


class Woman(models.Model):
    """ порядок, последовательность атрибутов влияет на отображение в форме """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Содержание")
    photo = models.ImageField(upload_to="photos/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT)  # запрещаем удалять категории у которых есть ссылки на категрию
    # добавил null=True так как данные уже были заполнены. А из-за связей миграция не проходила

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title  # если это не прописать, то в админ панели будет отображаться как объект. А так будет как текст

    def get_url(self):
        # return reverse("postt", kwargs={"id": self.pk})  # вариант через id
        return reverse("post_slug", kwargs={"post_slug": self.slug})  # через слаг

    def get_absolute_url(self):
        """ Необходим для админ панели """
        # return reverse("postt", kwargs={"id": self.pk})
        return reverse("post_slug", kwargs={"post_slug": self.slug})

    class Meta:
        """ в админке называние таблицы заменяет"""
        verbose_name = "известные женьщины"
        verbose_name_plural = "известные женьщины"  # джанго ко всем названиям добавляет букву s. переобпределяем чтобы избавить от этого
        ordering = ['-time_create', 'title']  # обратная сортировка по time_create.
        # таблица будет показана в таком виде и в админке и на основной странице
        # так же это важно для пагинации


class WomanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Woman
        fields = ('title', 'cat_id')


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="название категории")  # поле индексировано
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_url(self):
        """ эта функция в шаблоне """
        # return reverse("categoryy", kwargs={"id": self.pk})
        return reverse("category", kwargs={"cat_slug": self.slug})  # атрибут передается в urls.py

    def get_absolute_url(self):
        """ функция отображает в админке.  Необходим для создания ссылки на объекты """
        return reverse("categoryy", kwargs={"id": self.pk})

    class Meta:
        """ в админке называние таблицы заменяет"""
        verbose_name = "Категория"
        verbose_name_plural = "Категории"  # джанго ко всем названиям добавляет букву s. переобпределяем чтобы избавить от этого
        ordering = ['name']


class Human(models.Model):

    name = models.CharField(max_length=255, db_index=True)
    age = models.IntegerField()
    work = models.ForeignKey('Work', on_delete=models.PROTECT)


class Work(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    street = models.CharField(max_length=255)
    funcstr = models.TextField()
    # funcstr = models.FunctionField()

    def get_func(self):
        return pickle.dumps(self.funcstr)
        # return pickle.loads(str(self.funcstr))
        # f = pickle.loads(self.funcstr.encode('utf-8'))
        # f = pickle.loads(str.encode(self.funcstr))
        # return f
        # return codecs.encode(pickle.dumps(self.funcstr), "base64").decode()

    # def set_func(self, function):
        # self.funcstr = pickle.dumps(function)
        # self.funcstr = pickle.dumps(self.funcstr)

    # function = property(get_func, set_func)

