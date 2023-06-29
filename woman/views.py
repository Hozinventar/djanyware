# __all__ = ['index', "categories", "years",
#            "pagenotfound", "about", "addpage", "contact"
#            , "login", "show_posts", "show_category", "show_post_slug"
#            ]
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from .models import *
from .forms import *
from .utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics, viewsets
from rest_framework.views import APIView  # самый базовый функционал. все от него наследуются
from rest_framework.response import Response
from .models import WomanSerializer
from django.forms import model_to_dict  # метод возвращает словарь из модели

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    ]


# можно руками наследоваться от всех классов , что в ModelViewSet. А можно исключить не нужные миксины и ограничить до нужного поведения
class WomanViewSet(viewsets.ModelViewSet):
    """ CRUD. класс которые объеденяет все остальные generics, чтобы не дублировать код как представлен в классах ниже
    как по всей таблице так и по id
    https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
    """
    queryset = Woman.objects.all()
    serializer_class = WomanSerializer


class WomanApi(generics.ListAPIView):
    """ первый тестовый через сериализатор"""
    queryset = Woman.objects.all()
    serializer_class = WomanSerializer


class WomanApiList(generics.ListCreateAPIView):
    """ GET и POST запросы. тот же гет как в ListAPIView, но еще и пост """
    queryset = Woman.objects.all()
    serializer_class = WomanSerializer


class WomanApiUpdate(generics.UpdateAPIView):
    """Provides put and patch method handlers."""
    queryset = Woman.objects.all()
    serializer_class = WomanSerializer


class WomanApiCRUD(generics.RetrieveUpdateDestroyAPIView):
    """CRUD Но только по pk"""
    queryset = Woman.objects.all()
    serializer_class = WomanSerializer


# поиграться
class WomanApi2(APIView):
    """ Наследуемся от базового класса без сериализации"""
    def get(self, request):
        """ будет отвечать на гет запросы"""
        # return Response({'1': 2})
        queryset = Woman.objects.all().values()  #
        return Response(queryset)

    def post(self, request):
        """ если отправить пост, то вернет этот ответ. можно даже Json не передавать"""
        # return Response({'1': 2})
        data = request.data
        wm = Woman.objects.create(
            title=data['title'],
            content=data['content'],
            cat_id=data['cat_id']
        )
        return Response(model_to_dict(wm))


# поиграться
class WomanApi3(APIView):
    """ Наследуемся от базового класса со своим кастомным сериализатором
    Вот этот текст является DOC строкой. и появится в описании к методу
    """
    def get(self, request):
        queryset = Woman.objects.all()
        return Response(WomanSerializer2(queryset, many=True).data)  # many говорит, что будет не одна строка

    def post(self, request):
        """ если отправить пост, то вернет этот ответ. можно даже Json не передавать"""
        # return Response({'1': 2})
        data = request.data

        # Проверка корректность принятых данных
        seri = WomanSerializer2(data=data)
        seri.is_valid(raise_exception=True)  # ответ в виде json строки. Иначе будет как html

        # таким методом сразу создает в БД
        # wm = Woman.objects.create(
        #     title=data['title'],
        #     slug="asd",
        #     content=data['content'],
        #     cat_id=data['cat_id']
        # )
        # Таким способом просто принтуем и смотрим что сериализация прошла
        wm = Woman(**data)
        return Response(WomanSerializer2(wm).data)


# поиграться
class WomanApi4(APIView):
    """ методы создания и удаления
    """
    def get(self, request):
        queryset = Woman.objects.all()
        return Response(WomanSerializer4(queryset, many=True).data)  # many говорит, что будет не одна строка

    def post(self, request):
        # Проверка корректность принятых данных
        seri = WomanSerializer4(data=request.data)
        seri.is_valid(raise_exception=True)
        seri.save()  # это метод create в WomanSerializer4
        return Response(seri.data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response("Method not allowed")

        try:
            inst = Woman.objects.get(pk=pk)
        except:
            return Response("Method not allowed")

        seri = WomanSerializer4(data=request.data, instance=inst)  # сериализатор понимает что передан аргумент instance
        # и поэтому при вызове save он использует функцию Update
        seri.is_valid(raise_exception=True)
        seri.save()
        return Response(seri.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response("Method not allowed")

        try:
            inst = Woman.objects.get(pk=pk)
            inst.delete()
        except:
            return Response("Method not allowed")
        return Response(f"deleted {pk}")


class Home(DataMixin, ListView):
    """ выборка из модели происходит сразу и шаблону передается атрибут object_list"""
    paginate_by = 2  # пагинация встроена в ListView. сразу передаются paginator И page_obj
    model = Woman  # get_queryset возвражает все строки без фильтрации
    template_name = 'woman/index2.html'  # переопределить шаблон, по умолчнию называние это <имя приложения>/<имя модули>_list.html
    # как пример это woman/woman_list.html
    context_object_name = 'posts'  # чтобы переопределить атрибут object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        """ дополняет контекст , что формируется автоматически и дополняет нуными атрибутами для шаблона """
        context = super().get_context_data(**kwargs)
        # без Mixin
        # context['menu'] = menu
        # context['title'] = "женьщины"
        # context['selected'] = 0
        # return context

        c_def = self.get_user_context(title="Главная страница")
        return context | c_def

    def get_queryset(self):
        """ если шаблон принимает атрибут что указан в <context_object_name> или <object_list>
         , то тут можно переопределить выборку """
        # posts = Woman.objects.filter(is_published=True)
        # posts = super().get_queryset().filter(is_published=True)
        posts = super().get_queryset().filter(is_published=True).prefetch_related('cat')  # жадный запрос
        # позволяет избежать дополнительных запросов к категории. Особенно это актуально при ленивых запросах.
        # иначе на каждую запись был отдельных запрос на выборку категории.
        # print(posts)
        return posts


class ShowPost(DataMixin, DetailView):
    """ шаблон где атрибут передается в url. он же является ключом
    для отображения страницы по одной строке из БД """
    model = Woman
    template_name = "woman/post.html"
    slug_url_kwarg = 'post_slug'  # переопределить аргумент если в urls нужен другой. По умолчанию slug
    context_object_name = "post"  # атрибут что передается в шаблон

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # без Mixin
        # context['title'] =  context['post'] # в модели опредлен __str__
        # return context
        c_def = self.get_user_context(title=context['post'])
        return context | c_def


class CategoryBy(DataMixin, ListView):
    """ выборка из модели происходит сразу и шаблону передается атрибут object_list"""
    model = Woman  # get_queryset возвражает все строки без фильтрации
    template_name = 'woman/index2.html'  # переопределить шаблон, по умолчнию называние это <имя приложения>/<имя модули>_list.html
    # как пример это woman/woman_list.html
    context_object_name = 'posts'  # чтобы переопределить атрибут object_list
    allow_empty = False  # когда страница не найдена, то вернет 404

    def get_context_data(self, *, object_list=None, **kwargs):
        """ дополняет контекст , что формируется автоматически и дополняет нуными атрибутами для шаблона """
        context = super().get_context_data(**kwargs)
        # без Mixin
        # a = context["posts"][0].cat.__dict__  # {'_state': <django.db.models.base.ModelState object at 0x0000018D1595E6A0>, 'id': 1, 'name': 'Актрисы', 'slug': 'aktrisy'}
        # b = context["posts"][0].cat_id
        # context['menu'] = menu
        # context['title'] = "Категория - " + str(context["posts"][0].cat)  # cat - будет названием категории
        # context['selected'] = context["posts"][0].cat_id  # cat_id будет число, индекс, он же ключ
        # return context

        # когда не используем жадную операцию
        title = "Категория - " + str(context["posts"][0].cat)  # cat - будет названием категории
        selected = context["posts"][0].cat_id  # cat_id будет число, индекс, он же ключ

        # print(context["categ"])
        c_def = self.get_user_context(title=title, selected=selected)

        return context | c_def

    def get_queryset(self):
        """ если шаблон принимает атрибут что указан в <context_object_name> или <object_list>
         , то тут можно переопределить выборку
         необходимо в модели так же скорректировать функцию get_url, где прописан reverse
         """
        posts = super().get_queryset().filter(cat__slug=self.kwargs["cat_slug"], is_published=True).prefetch_related('cat')  # cat_slug берется из urls. где указан атрибут для рута
        # cat__slug  означает как обращение к атрибуту cat.slug
        # print(posts)
        return posts


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """ добавить статью на сайт """
    form_class = PostForm  # класс формы который будет отображаться в темлейте
    template_name = "woman/addpage.html"
    success_url = reverse_lazy("home")  # переопределяет на какую страницу перейти после добавления записи
    login_url = reverse_lazy("admin")  # только когда есть mixin login. перенаправить если не авторизован

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # без Mixin
        # context['menu'] = menu
        # context['title'] = "Добавление статьи"
        # return context
        c_def = self.get_user_context(title="Добавление статьи")
        return context | c_def  # суммирует славари


class RegisterUser(DataMixin, CreateView):
    """ авторизация на сайте через форму """
    # form_class = UserCreationForm  # стандартная форма из коробки от джанго. можно прям так подставить
    form_class = RegisterUserForm  # переопределили стандартную форму

    template_name = "woman/register.html"
    # success_url = reverse_lazy("login")  # переопределяет на какую страницу перейти после добавления записи
    # но когда есть функция form_valid этот редирект не работает

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация ")
        return context | c_def

    def form_valid(self, form):
        """ если после регистрации мы хотим сразу перенаправлять на нужную старницу при этом сразу авторизовавшись."""
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    # form_class = AuthenticationForm  # переопределили стандартную форму
    form_class = LoginUserForm  # либо наследуемся от собственной
    template_name = "woman/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return context | c_def

    def get_success_url(self):
        """ в случае успешной авторизации перенаправлять на указанную страницу
        иначе перенаправляет на http://127.0.0.1:8000/accounts/profile/
        """
        return reverse_lazy("home")


class ContactView(DataMixin, FormView):
    """
    FormView - для форм которые не привязаны к модели
    """
    form_class = ContactForm
    template_name = "woman/contact.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return context | c_def

    def form_valid(self, form):
        """ если после регистрации мы хотим сразу перенаправлять на нужную старницу при этом сразу авторизовавшись."""
        print(form.cleaned_data)  # отображает словарь когда будет post через форму
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def index(request):
    posts = Woman.objects.all()
    cats = Category.objects.all()
    context = {"text": "начальная страница",
               "title": "главная страница Девушки",
               "posts": posts,
               "categ": cats,
               "selected": 0,
                "menu": menu
               }
    return render(request, "woman/index.html", context=context)


def addpage_(request):
    """ когда форма не связана с БД приходится писать так"""
    if request.method == "POST":
        form = PostFormOld(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)  # Покажет словарь из заполненных атрибутов

            try:
                Woman.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления')
    else:
        form = PostForm()
    context = {
       "title": "Добавление статьи",
        "menu": menu,
        'form': form
               }
    return render(request, "woman/addpage.html", context=context)


def addpage(request):
    """ форма связана с БД + передаются файлы"""
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {
       "title": "Добавление статьи",
        "menu": menu,
        'form': form
               }
    return render(request, "woman/addpage.html", context=context)


def about(request):
    return render(request, "woman/about.html")


def categories(request, id):
    a = request.GET
    print(a, a.get("asd"), sep="\n")
    print(str(a))
    return HttpResponse(f"Страница {id} приложения categories {str(dict(a))}")


def years(request, year):
    print(type(year))
    if int(year) < 2000:
        raise Http404()
    if int(year) == 2000:
        return redirect("home")  # по именими представляения в urls приложения
    return HttpResponse(f"Страница {year} приложения categories")


def show_posts(request, id):
    # text = Woman.objectWoman.objects.get(pk=id).title
    # return HttpResponse(f"строка {id}")
    post = get_object_or_404(Woman, pk=id)
    context = {
               "title": post.title,
               "post": post,
               "menu": menu,
               "selected": post.cat_id,
               }
    return render(request, "woman/post.html", context=context)


def show_post_slug(request, post_slug):
    # text = Woman.objectWoman.objects.get(pk=id).title
    # return HttpResponse(f"строка {id}")
    post = get_object_or_404(Woman, slug=post_slug)
    context = {
               "title": post.title,
               "post": post,
               "menu": menu,
               "selected": post.cat_id,
               }
    return render(request, "woman/post.html", context=context)


def show_by_category(request, id):
    """ отобразить статьи на основе категории"""
    # posts = Woman.objects.filter(cat_id=id)
    # cats = Category.objects.all()  # в шаблоне импортируется тег. можно от сюда его убрать.
    context = {"text": "начальная страница",
               "title": "главная страница Девушки",
               # "posts": posts,
               # "categ": cats,
               "selected": id,
                "menu": menu
               }
    return render(request, "woman/index.html", context=context)
    # return render(request, "woman/base.html", context=context)


def pagenotfound(request, exception):
    return HttpResponseNotFound(f"Страница не найдена")
