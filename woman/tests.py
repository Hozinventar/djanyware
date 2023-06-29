# from django.test import TestCase
import requests as r

# res = r.post("http://127.0.0.1:8000/api/v1/womans2", json={"title": "девочка", "cat_id": "1"})
# print(res.text)
# Create your tests here.
# res = r.post("http://127.0.0.1:8000/api/v1/womans4", json={"title": "erunda", "cat_id": "1", "content": "sdfsdf"})
# res = r.post("http://127.0.0.1:8000/api/v1/womans4", json={"title": "erunda", "content": "sdfsdf"})  # не указываем обязательное поле {"cat_id":["Это поле обязательно для заполнения."]}
# print(res.text)

res = r.put("http://127.0.0.1:8000/api/v1/womanslist/6/", json={"title": "erunda2", "cat": "2", "content": "sdfsdf"})

# res = r.put("http://127.0.0.1:8000/api/v1/womans4/50/", json={"title": "erunda", "content": "sdfsdf2", "cat_id": "1"})  # не указываем обязательное поле {"cat_id":["Это поле обязательно для заполнения."]}
# res = r.delete("http://127.0.0.1:8000/api/v1/womans4/5/")  # не указываем обязательное поле {"cat_id":["Это поле обязательно для заполнения."]}
print(res.text)
print(res.status_code)
