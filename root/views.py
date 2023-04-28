from django.shortcuts import render
from django.http import HttpResponse


def root(request):
    return HttpResponse("<h1>начальная страница</h1>")

# Create your views here.
