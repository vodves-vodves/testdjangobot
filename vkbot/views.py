from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def main(request):
    if request.method == "GET":
        return HttpResponse({"message": "hello world!"})
    elif request.method == 'POST':
        data = request.data
        print(data)
