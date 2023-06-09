# from django.test import TestCase
import requests as r

# res = r.post("http://127.0.0.1:8000/api/v1/womans2", json={"title": "девочка", "cat_id": "1"})
# print(res.text)
# Create your tests here.
# res = r.post("http://127.0.0.1:8000/api/v1/womans3", json={"title": "erunda", "cat_id": "1", "content": "sdfsdf"})
res = r.post("http://127.0.0.1:8000/api/v1/womans3", json={"title": "erunda", "content": "sdfsdf"})  # не указываем обязательное поле {"cat_id":["Это поле обязательно для заполнения."]}
print(res.text)
