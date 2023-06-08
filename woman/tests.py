# from django.test import TestCase
import requests as r

res = r.post("http://127.0.0.1:8000/api/v1/womans2", json={"title": "девочка", "cat_id": "1"})
print(res.text)
# Create your tests here.
