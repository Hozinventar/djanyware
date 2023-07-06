from rest_framework.pagination import PageNumberPagination


class WomanApiListPagin(PageNumberPagination):
    page_size = 1  # колличество строк на страницу
    page_size_query_param = 'page_size'  # если пользователь хочет расширить вывод , то добавляет этот параметр в гет запрос
    # r = requests.get('http://127.0.0.1:8000/api/v1/womansgetpost?page_size=3', headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {act}'})
    max_page_size = 10000  # ограничиваем page_size не больше этого числа, чтобы пользователь не наглел.