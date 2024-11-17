from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView


def test_home(request):
    return HttpResponse('<h1>Test Home</h1>')
