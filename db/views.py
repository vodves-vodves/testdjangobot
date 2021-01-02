from django.http import HttpResponse
from db.settings import CONFIRMATION_TOKEN


def main(request):
    if request.method == "GET":
        return HttpResponse({"message": "hello world!"})
    elif request.method == 'POST':
        data = request.data
        print(data)
        if data["type"] == "confirmation":
            return HttpResponse(CONFIRMATION_TOKEN)
