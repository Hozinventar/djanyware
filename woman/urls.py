from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page
from .views import *
from rest_framework import routers, urls

# rout = routers.SimpleRouter()
rout = routers.DefaultRouter()  # если обратиться к корневому url , то покажет все доступные url для методов
# rout.register(r'womans', WomanViewSet)  # регистрируем рутер , чтобы затем использовать ViewSet и не дулировать строки с pk id
rout.register(r'womans', WomanViewSet, basename='woman')  # basename когда в WomanViewSet необходимо переопределить queryset на get_queryset,
# то в WomanViewSet queryset можно закоментировать, но тогда в basename прописать имя модели.
print(rout.urls)  # url генерируется на основе имени модели


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
    path('api/v1/', include(urls)),  # дефолтные маршруты rest_framework
    path('api/v1/', include(rout.urls)),  # стандартный простой способ создать api по таблице. внимательно рут указан в rout. не тут
    path('api/v1/womansmodels', WomanViewSet.as_view({'get': 'list'})),  # необходимо указывать и переопределять методы
    path('api/v1/womansmodels/<int:pk>/', WomanViewSet.as_view({'put': 'update'})),
    path('api/v1/womanss', WomanApi.as_view()),
    path('api/v1/womansgetpost', WomanApiList.as_view()),
    path('api/v1/womanslist/<int:pk>/', WomanApiUpdate.as_view()),
    path('api/v1/womanscrud/<int:pk>/', WomanApiCRUD.as_view()),
    path('api/v1/womans2', WomanApi2.as_view()),
    path('api/v1/womans3', WomanApi3.as_view()),
    path('api/v1/womans4', WomanApi4.as_view()),
    path('api/v1/womans4/<int:pk>/', WomanApi4.as_view()),  # тестируем PUT
    path('api/v1/womangetpermisson', WomanApiListPermission.as_view()),
    path('api/v1/womanupdatepermisson/<int:pk>/', WomanApiUpdatePermission.as_view()),
    path('api/v1/womandelpermisson/<int:pk>/', WomanApiCDestroyPermission.as_view()),



]
