from django.shortcuts import render, HttpResponse

# Testing Testing Please Disregard

# Create your views here.
def home(request):
    return HttpResponse("hello world!")