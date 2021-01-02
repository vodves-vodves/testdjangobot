from django.http import HttpResponse
from db.settings import CONFIRMATION_TOKEN
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def main(request):
    if request.method == "GET":
        return HttpResponse({"message": "hello world!"})
    elif request.method == 'POST':
        data = request.data
        print(data)
        if data["type"] == "confirmation":
            return HttpResponse(CONFIRMATION_TOKEN)
