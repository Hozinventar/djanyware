from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    # path('', index, name="home"),  # Начальная страница. Name переопределяет rout
    path('', Home.as_view(), name="home"),  # Начальная страница через класс
    # path('', cache_page(60)(Home.as_view()), name="home"),  # кушируем всю страницу на 60 секунд
    path('cats/<int:id>/', categories),  # http://127.0.0.1:8000/women/cats/1/?asd=wer
    re_path(r'^years/(?P<year>[0-9]{4})/', years),  # http://127.0.0.1:8000/women/years/2990/
    path('about/', about, name="about"),  # http://127.0.0.1:8000/about
    # path('addpage/', addpage, name="add_page"),
    path('addpage/', AddPage.as_view(), name="add_page"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),
    path('register/', RegisterUser.as_view(), name="register"),
    # path('post/<int:id>/', show_posts, name="postt"),
    # path('post/<slug:post_slug>/', show_post_slug, name="post_slug"),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name="post_slug"),
    # path('category/<int:id>/', show_by_category, name="categoryy"),  # через функцию
    path('category/<slug:cat_slug>/', CategoryBy.as_view(), name="category"),
    path('api/v1/womans', WomanApi.as_view()),
    path('api/v1/womans2', WomanApi2.as_view())
]
